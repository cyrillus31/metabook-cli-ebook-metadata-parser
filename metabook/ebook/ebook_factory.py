import os

from ebook.abstract_ebook import Ebook
from ebook.epub import EPUB_book
from ebook.fb2 import FB2_book
from exceptions import ExtNotSupportedError

EXTENSIONS = {
    ".epub": EPUB_book,
    ".fb2": FB2_book,
}


def ebook_factory(file_path: str, verbose: bool = False) -> Ebook:
    _, extension = os.path.splitext(file_path)
    if extension in EXTENSIONS:
        return EXTENSIONS[extension](file_path, verbose)
    raise ExtNotSupportedError(extension)
