from ebook import Ebook, BookMetaData

class EbookParser:
    def __init__(self) -> None:
        pass

    def get_metadata(self, book: Ebook) -> BookMetaData:
        with book as content:
            md = content.get_metadata()
        return md
