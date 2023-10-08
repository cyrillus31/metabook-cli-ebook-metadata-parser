import sys

sys.dont_write_bytecode = True

from parser import EbookParser
from ebook import ebook_factory
from cli import get_cli_arguments


if __name__ == "__main__":
    args = get_cli_arguments()
    files = args.filename
    verbose = args.verbose
    ebook_parser = EbookParser()
    for file in files:
        ebook = ebook_factory(file, verbose)
        print(ebook_parser.get_metadata(ebook))
