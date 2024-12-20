import csv


class CSVHandler:
    def read_csv(self, filepath, delimiter=',', has_header=True):
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=delimiter)
            data = list(reader)
            return data


