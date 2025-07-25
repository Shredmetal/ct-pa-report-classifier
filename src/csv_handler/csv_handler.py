import csv
import os
from argparse import ArgumentError
from typing import List, Dict, Any


class CSVHandler:

    @staticmethod

    def read_csv(file_path: str) -> List[Dict[str, str]]:

        reports = []
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                reports.append(row)

        return reports

    @staticmethod
    def write_to_csv(data: Dict[str, Any], write_path: str) -> None:
        os.makedirs(os.path.dirname(write_path), exist_ok=True)

        file_exists = os.path.isfile(write_path)
        mode = 'a' if file_exists else 'w'

        # Extract fieldnames dynamically from the dictionary
        fieldnames = list(data.keys())

        with open(write_path, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(data)