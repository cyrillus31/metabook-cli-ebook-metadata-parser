import os
import shutil
import xml.etree.ElementTree as ET
import argparse
from dataclasses import dataclass

argparser = argparse.ArgumentParser(
    prog="E-book metadata parser",
    description="Returns title, author, publisher and date published from a specified EPUB or FB2 file",
    epilog="P.S. Developed as part of a take-home assignment",
)
argparser.add_argument("filename", help="Insert a file", nargs="+", type=lambda p: p if os.path.isabs(p) else os.path.abspath(p)) 
# argparser.add_argument("-v", "--verbose", help="Displays additional information", required=False)

args = argparser.parse_args()
print(args.filename)

@dataclass
class BookMetaData:
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    date_published: str | None = None

    def __str__(self):
        return f"\nTitle: {self.title}\nAuthor: {self.author}\nPublisher: {self.publisher}\nDate published: {self.date_published}"


def find_opf(folder: str) -> str:
    for root, folders, files in os.walk(folder):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == ".opf":
                return os.path.join(root, file)


def parse_metadata(file, extension):
    meta = BookMetaData()
    tree = ET.parse(file)
    root = tree.getroot()
    # print(root.tag)
    namespace = "{http://www.idpf.org/2007/opf}"
    metadata_xml = root.find(f"{namespace}metadata")

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

    return meta


if __name__ == "__main__":
    for file in args.filename:
        absolute_path, extension = os.path.splitext(file)
        name = os.path.basename(file)
        root = os.path.dirname(file)
        folder_name = f".{name}"
        if extension in [".epub", ".fb2"]:
            os.makedirs(folder_name)
            shutil.unpack_archive(file, extract_dir=folder_name, format="zip")
            folder_path = os.path.join(root, folder_name)
            metadata_file = find_opf(folder_path)
            metadata = parse_metadata(metadata_file, extension)
            shutil.rmtree(folder_name)
            print(metadata)


