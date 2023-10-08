import os
import argparse
import sys

sys.dont_write_bytecode = True

from parser import EbookParser
from ebook import EPUB_book


ebook_parser = EbookParser()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="E-book metadata parser",
        description="Returns title, author, publisher and date published from a specified EPUB or FB2",
        epilog="P.S. Developed as part of a take-home assignment",
    )
    argparser.add_argument(
        "filename",
        help="Insert a relative or absolute filepaths",
        nargs="+",
        default=None,
        type=lambda p: p if os.path.isabs(p) else os.path.abspath(p),
    )
    # argparser.add_argument("-v", "--verbose", help="Displays additional information", required=False)

    args = argparser.parse_args()
    files = args.filename
    # print(files)

    if files == [None]:
        root, folders, files = next(os.walk(os.getcwd()))

    for file in files:
        ebook = EPUB_book(file)
        print(ebook_parser.get_metadata(ebook))
