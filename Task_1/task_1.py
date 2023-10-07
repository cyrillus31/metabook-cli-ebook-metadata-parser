import os
import csv
import shutil

import unzip

root, folders, files = next(os.walk(os.getcwd()))

files = (os.path.join(root, file) for file in files if ".csv" in file)

result = {}

def parse_file(file) -> dict:
    frequency_counter = {}
    result = {}
    with open(file, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        # to skip the header
        next(csv_reader)
        for row in csv_reader:
            cache, id = row
            count = frequency_counter.get(id, 0) + 1
            frequency_counter[id] = count
            if count > 1:
                result[count-1].remove(id)
            set_of_ids = result.get(count, set())
            set_of_ids.add(id)
            result[count] = set_of_ids
        return result


for file in files:
    result = parse_file(file)
    print(f"\nFollwoing ids were encountered 3 times: {result[3]}")
    for key in result:
        print(f"\nHere's how many ids repreat {key} times: {len(result[key])}")
 
