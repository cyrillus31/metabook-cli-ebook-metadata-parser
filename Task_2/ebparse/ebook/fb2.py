import xml.etree.ElementTree as ET

from ebook.abstract_ebook import Ebook
from ebook.metadata_dataclass import BookMetaData
from exceptions import UnexpectedXMLStructureError



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
