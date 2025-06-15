import csv
import os
from typing import List, Dict, Any


class CSVHandler:

    @staticmethod
    def read_csv(file_path: str) -> List[str]:

        reports = []

        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                if row:
                    reports.append(row[0])

        return reports

    @staticmethod
    def write_to_csv(data: Dict[str, Any], write_path: str):
        os.makedirs(os.path.dirname(write_path), exist_ok=True)

        file_exists = os.path.isfile(write_path)
        mode = 'a' if file_exists else 'w'

        with open(write_path, mode, newline='', encoding='utf-8') as csvfile:
            fieldnames = ['report', 'pneumonia_present', 'pneumonia_laterality', 'pneumonia_size']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(data)