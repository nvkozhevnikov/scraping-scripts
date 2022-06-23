import csv

class CsvHandler:
    def __init__(self, filename):
        self.filename = filename

    def create_headers_csv_semicolon(self, headers: list) -> None:
        ''' Create csv file with headers, delimiter is semicolon '''
        with open(self.filename, 'w', encoding='UTF-8', newline='') as f:
            csv.DictWriter(f, fieldnames=headers, delimiter=';').writeheader()

    def write_to_csv_semicolon(self, data: dict) -> None:
        ''' Add new fields to csv, delimiter is semicolon, one entry is one line (row) '''
        with open(self.filename, 'a', encoding='UTF-8', newline='') as f:
            csv.DictWriter(f, fieldnames=list(data), delimiter=';').writerow(data)

    def read_csv_semicolon(self) -> list:
        ''' Get data by reading csv file, delimiter is semicolon, returns a list of dictionaries '''
        data = []
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                data.append(row)
            return data