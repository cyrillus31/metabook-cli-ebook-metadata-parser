import os
import argparse


def get_cli_arguments():
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
    return files

# print(files)

# if files == [None]:
#     root, folders, files = next(os.walk(os.getcwd()))
