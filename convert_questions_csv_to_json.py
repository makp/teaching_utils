import csv
import json
import ast

def csv_to_json(csv_file_path, json_file_path):
    data = []

    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            row['mc_options'] = ast.literal_eval(row['mc_options'])
            row['subject'] = ast.literal_eval(row['subject'])
            data.append(row)

    with open(json_file_path, mode='w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2)
