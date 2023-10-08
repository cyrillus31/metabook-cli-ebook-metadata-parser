from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
import shutil
import xml.etree.ElementTree as ET


from exceptions import NotEbookError, OPFNotFoundError, ExtNotSupportedError, UnexpectedXMLStructureError





@dataclass
class BookMetaData:
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    date_published: str | None = None

    def __str__(self):
        return f"\nTitle: {self.title}\nAuthor: {self.author}\nPublisher: {self.publisher}\nDate published: {self.date_published}"


class Ebook(ABC):
    @abstractmethod
    def get_metadata(self) -> BookMetaData:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self) -> None:
        raise NotImplementedError


class EPUB_book(Ebook):
    def __init__(self, absolute_path: str) -> None:
        self.ebook_path = absolute_path
        self.namespace = "{http://www.idpf.org/2007/opf}"

    def __enter__(self) -> Ebook:
        # print("open")
        name = os.path.basename(self.ebook_path)
        root = os.path.dirname(self.ebook_path)

        # create temporary folder for the ebook to be unzipped into
        temp_folder_name = f".{name}"
        os.makedirs(temp_folder_name)
        self.temp_folder_path = os.path.join(root, temp_folder_name)

        # unzip the ebook
        try:
            shutil.unpack_archive(
                self.ebook_path, extract_dir=temp_folder_name, format="zip"
            )
        except (shutil.ReadError, OPFNotFoundError):
            pass
        # metadata_file = find_opf(folder_path)
        # self.metadata = parse_metadata(metadata_file, extension)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # print(exc_type, exc_value)
        shutil.rmtree(self.temp_folder_path)
        if exc_type is OPFNotFoundError:
            raise NotEbookError



    def _find_opf(self) -> str:
        for root, folders, files in os.walk(self.temp_folder_path):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == ".opf":
                    return os.path.join(root, file)
        raise OPFNotFoundError

    def get_metadata(self) -> BookMetaData:
        opf_path = self._find_opf()
        meta = BookMetaData()

        tree = ET.parse(opf_path)
        root = tree.getroot()
        # print(root.tag)
        metadata_xml = root.find(f"{self.namespace}metadata")

        if not metadata_xml:
            raise Exception("Metadata was not found within the .opf file")

        for child in metadata_xml:
            text, tag = child.text, child.tag

            if "title" in tag:
                meta.title = text
            elif "creator" in tag:
                meta.author = text
            elif "publisher" in tag:
                meta.publisher = text
            elif "date" in tag:
                meta.date_published = text

        self.metadata = meta
        return self.metadata


class FB2_book(Ebook):
    def __init__(self, absolute_path: str) -> None:
        self.ebook_path = absolute_path
        self.namespace = "{http://www.gribuser.ru/xml/fictionbook/2.0}"
        self.meta = BookMetaData()

    def __enter__(self) -> Ebook:
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def get_metadata(self) -> BookMetaData:

        tree = ET.parse(self.ebook_path)
        root = tree.getroot()
        description = root.find(f"{self.namespace}description")
        if not description:
            raise UnexpectedXMLStructureError

        title_info = description.find(f"{self.namespace}title-info")
        publish_info = description.find((f"{self.namespace}publish-info"))


        for title_info_child in title_info.iter():
            tag = title_info_child.tag
            if "author" in tag:
                self.meta.author = " ".join((string.text for string in title_info_child.iter())).strip()
            elif "title" in tag:
                self.title = title_info_child.text

        for publish_info_child in publish_info.iter():
            tag = publish_info_child.tag
            if "publisher" in tag:
                self.meta.publisher = publish_info_child.text
            elif "year" in tag:
                self.meta.date_published = publish_info_child.text


        # author = " ".join([name_part.text for name_part in title_info.find(f"{self.namespace}author")])
        # title = title_info.find(f"{self.namespace}book-title").text
        # publisher = publish_info.find(f"{self.namespace}publisher").text
        # date_published = publish_info.find(f"{self.namespace}year").text

        # meta.author = author
        # meta.title = title
        # meta.publisher = publisher
        # meta.date_published = date_published
        

        return self.meta


EXTENSIONS = {
        ".epub": EPUB_book,
        ".fb2": FB2_book,
        }

def ebook_factory(file_path: str) -> Ebook:
    rest, extension = os.path.splitext(file_path)
    if extension in EXTENSIONS:
        return EXTENSIONS[extension](file_path)
    raise ExtNotSupportedError(extension)






