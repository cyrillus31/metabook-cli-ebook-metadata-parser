import shutil
import os

root, folders, files = next(os.walk(os.getcwd()))

for file in files:
    if ".zip" in file:
        shutil.unpack_archive(file)

