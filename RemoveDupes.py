import csv
import re

with open('database.csv', 'r', encoding='utf-8') as in_file, open('cleaned_database.csv', 'w') as out_file:
    seen = set()

    
    fields = ["full-image", "label-image", "tags", "height", "width", "clicks"]

    output_writer = csv.DictWriter(out_file, fieldnames=fields)

    output_writer.writeheader()

    for line in in_file:
        
        try:
            object = {
                "full-image": line.split(',')[0],
                "label-image": line.split(',')[1],
                "tags": re.sub(r"[^0-9a-zA-Z:,\s]+", "", line.split(',')[2]),
                "height": line.split(",")[3],
                "width": line.split(",")[4],
                "clicks": 0
            }
        except:
            continue
        
        if object["label-image"] in seen:
            continue

        seen.add(object["label-image"])
        try:
            output_writer.writerow(object)
        except UnicodeEncodeError:
            continue
