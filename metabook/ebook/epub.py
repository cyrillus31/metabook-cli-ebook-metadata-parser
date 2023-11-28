import os
import shutil
import xml.etree.ElementTree as ET

from ebook.abstract_ebook import Ebook
from ebook.metadata_dataclass import BookMetaData
from exceptions import OPFNotFoundError


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
