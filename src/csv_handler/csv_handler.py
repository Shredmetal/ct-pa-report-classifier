import csv
import os
from argparse import ArgumentError
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
    def write_to_csv(data: Dict[str, Any], write_path: str, output_type:str) -> None:
        os.makedirs(os.path.dirname(write_path), exist_ok=True)

        file_exists = os.path.isfile(write_path)
        mode = 'a' if file_exists else 'w'

        if output_type == 'pe':
            with open(write_path, mode, newline='', encoding='utf-8') as csvfile:
                fieldnames = ['report', 'pe_presence', 'pe_large', 'pe_saddle', 'pe_laterality', 'heart_strain']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                writer.writerow(data)

        elif output_type == 'lung_abnormality':
            with open(write_path, mode, newline='', encoding='utf-8') as csvfile:
                fieldnames = ['report', 'lung_abnormality', 'lung_bronchiectasis', 'lung_emphysema', 'lung_bullae', 'other_abnormality']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                writer.writerow(data)

        else:
            raise ArgumentError("output_type must be 'pe' or 'lung_abnormality'")