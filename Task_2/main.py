import os
import shutil
import xml.etree.ElementTree as ET
from dataclasses import dataclass


def find_opf(folder: str) -> str:
    for root, folders, files in os.walk(folder):
        if "OEBPS" not in root:
            continue
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext == ".opf":
                return os.path.join(root, file)

@dataclass
class MetaDataClass:
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    date_published: str | None = None

    def __str__(self):
        return f"\nTitle: {self.title}\nAuthor: {self.author}\nPublisher: {self.publisher}\nDate published: {self.date_published}"

def parse_metadata(file, extension):
    meta = MetaDataClass()
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


root, folders, files = next(os.walk(os.getcwd()))

for file in files:
    name, extension = os.path.splitext(file)
    folder_name = f".{name}"
    if extension in [".epub", ".fb2"]:
        os.makedirs(folder_name)
        shutil.unpack_archive(file, extract_dir=folder_name, format="zip")
        folder_path = os.path.join(root, folder_name)
        metadata_file = find_opf(folder_path)
        metadata = parse_metadata(metadata_file, extension)
        shutil.rmtree(folder_name)
        print(metadata)


if __name__ == "__main__":
    pass
