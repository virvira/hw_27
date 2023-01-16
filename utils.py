import csv
import json
from typing import List

ads_csv_file = 'data/ads.csv'
categories_csv_file = 'data/categories.csv'

ads_json_file = 'data/ads.json'
categories_json_file = 'data/categories.json'


def moveCsvToJson(csv_file, json_file, model) -> None:
    data = []
    with open(csv_file, 'r', encoding='utf-8') as csv_f:
        csv_reader = csv.DictReader(csv_f)
        for row in csv_reader:
            row_id = row['id']
            record = {"model": model, "pk": row_id}

            if "price" in row:
                row["price"] = int(row["price"])

            if "is_published" in row:
                row["is_published"] = bool(row["is_published"])
            record["fields"] = row
            data.append(record)

    with open(json_file, 'w', encoding='utf-8') as json_f:
        json_f.write(json.dumps(data, indent=4, ensure_ascii=False))


moveCsvToJson(categories_csv_file, categories_json_file, 'ads.category')
moveCsvToJson(ads_csv_file, ads_json_file, 'ads.advertisement')
