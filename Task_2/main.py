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

def parse_metadata(file, extension):

    @dataclass
    class MetaDataClass:
        title: str | None
        author: str | None
        publisher: str | None
        date_published: str | None

    meta = MetaDataClass()
    tree = ET.parse(file)
    root = tree.getroot()
    metadata = root.find('metadata')
    meta.title = metadata.find('dc:title').text
    meta.author = metadata.find('dc:creator').text
    meta.publisher = metadata.find('dc:publisher').text
    meta.date_published = metadata.find('dc:date').text 
    return meta


root, folders, files = next(os.walk(os.getcwd()))

for file in files:
    name, extension = os.path.splitext(file)
    if extension in [".epub", ".fb2"]:
        os.makedirs(name)
        shutil.unpack_archive(file, extract_dir=name,  format="zip")
        folder_path = os.path.join(root, name)
        metadata_file = find_opf(folder_path)
        metadata = parse_metadata(metadata_file, extension)
        print(metadata)









if __name__ == "__main__":
    pass
    









