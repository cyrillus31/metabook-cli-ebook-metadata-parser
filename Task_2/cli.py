import os
import argparse


def get_cli_arguments():
    argparser = argparse.ArgumentParser(
        prog="E-book metadata parser",
        description="Returns title, author, publisher and date published from a specified EPUB or FB2",
        epilog="P.S. Developed as part of a take-home assignment by kirill.olegovich31@gmail.com",
    )

    argparser.add_argument(
        "filename",
        help="Insert a relative or absolute filepaths",
        nargs="+",
        default=None,
        type=lambda p: p if os.path.isabs(p) else os.path.abspath(p),
    )

    argparser.add_argument("-v", "--verbose", help="Display additional information", required=False, action="store_true")

    args = argparser.parse_args()
    return args


# print(files)

# if files == [None]:
#     root, folders, files = next(os.walk(os.getcwd()))
