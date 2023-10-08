from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
import shutil
import xml.etree.ElementTree as ET


from exceptions import (
    NotEbookError,
    OPFNotFoundError,
    ExtNotSupportedError,
    UnexpectedXMLStructureError,
)


@dataclass
class BookMetaData:
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    date_published: str | None = None
    description: str | None = None
    language: str | None = None

    verbose: bool = False

    def __str__(self):
        if not self.verbose:
            return f"""
Title: {self.title}
Author: {self.author}
Publisher: {self.publisher}
Date published: {self.date_published}"""

        return f"""
Title: {self.title}
Author: {self.author}
Publisher: {self.publisher}
Date published: {self.date_published}
Language: {self.language}
Description: {self.description}
"""


class Ebook(ABC):
    @abstractmethod
    def get_metadata(self) -> BookMetaData:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        raise NotImplementedError


class EPUB_book(Ebook):
    def __init__(self, absolute_path: str, verbose: bool = False) -> None:
        self.ebook_path = absolute_path
        self.namespace = "{http://www.idpf.org/2007/opf}"
        self.metadata = BookMetaData(verbose=verbose)

    def __enter__(self) -> Ebook:
        """This method creates a temporary folder containing unzipped files of the book to be parsed"""
        name = os.path.basename(self.ebook_path)
        root = os.path.dirname(self.ebook_path)

        # create temporary folder for the ebook to be unzipped into
        temp_folder_name = f".{name}"
        self.temp_folder_path = os.path.join(root, temp_folder_name)
        os.makedirs(self.temp_folder_path)

        # unzip the ebook
        try:
            shutil.unpack_archive(
                self.ebook_path, extract_dir=self.temp_folder_path, format="zip"
            )
        except (shutil.ReadError, OPFNotFoundError):
            pass
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """This method deletes the temporary folder containing unzipped files of the book"""
        shutil.rmtree(self.temp_folder_path)
        if exc_type is OPFNotFoundError:
            raise exc_type

    def _find_opf(self) -> str:
        """Searches the temporary folder for the .OPF file that can be parsed with xml parser"""
        for root, folders, files in os.walk(self.temp_folder_path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == ".opf":
                    return os.path.join(root, file)
        raise OPFNotFoundError

    def get_metadata(self) -> BookMetaData:
        opf_path = self._find_opf()

        tree = ET.parse(opf_path)
        root = tree.getroot()
        # print(root.tag)
        metadata_xml = root.find(f"{self.namespace}metadata")

        if not metadata_xml:
            raise Exception("Metadata was not found within the .opf file")

        for child in metadata_xml:
            text, tag = child.text, child.tag

            if "title" in tag:
                self.metadata.title = text
            elif "creator" in tag:
                self.metadata.author = text
            elif "publisher" in tag:
                self.metadata.publisher = text
            elif "date" in tag:
                self.metadata.date_published = text
            elif "language" in tag:
                self.metadata.language = text
            elif "description" in tag:
                self.metadata.description = text

        return self.metadata


class FB2_book(Ebook):
    def __init__(self, absolute_path: str, verbose: bool = False) -> None:
        self.ebook_path = absolute_path
        self.namespace = "{http://www.gribuser.ru/xml/fictionbook/2.0}"
        self.metadata = BookMetaData(verbose=verbose)

    def __enter__(self) -> Ebook:
        """Unlike EPUB, FB2 doesn't require unzipping so this method jsut returns self"""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def get_metadata(self) -> BookMetaData:
        """This method parses XML and returns specified metadata"""
        tree = ET.parse(self.ebook_path)
        root = tree.getroot()
        description = root.find(f"{self.namespace}description")

        if not description:
            raise UnexpectedXMLStructureError

        title_info = description.find(f"{self.namespace}title-info")
        publish_info = description.find((f"{self.namespace}publish-info"))

        if title_info:
            for title_info_child in title_info.iter():
                tag = title_info_child.tag
                if "author" in tag:
                    self.metadata.author = " ".join(
                        (string.text for string in title_info_child.iter())
                    ).strip()
                elif "book-title" in tag:
                    self.metadata.title = title_info_child.text
                elif "annotation" in tag:
                    self.metadata.description = "".join(title_info_child.itertext())
                elif ("lang" in tag) and ("src-lang" not in tag):
                    self.metadata.language = title_info_child.text.strip()

        if publish_info:
            for publish_info_child in publish_info.iter():
                tag = publish_info_child.tag
                if "publisher" in tag:
                    self.metadata.publisher = publish_info_child.text
                elif "year" in tag:
                    self.metadata.date_published = publish_info_child.text

        return self.metadata


EXTENSIONS = {
    ".epub": EPUB_book,
    ".fb2": FB2_book,
}


def ebook_factory(file_path: str, verbose: bool = False) -> Ebook:
    _, extension = os.path.splitext(file_path)
    if extension in EXTENSIONS:
        return EXTENSIONS[extension](file_path, verbose)
    raise ExtNotSupportedError(extension)
