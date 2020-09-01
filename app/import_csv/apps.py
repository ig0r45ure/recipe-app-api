from django.apps import AppConfig

import csv


class ImportCsvConfig(AppConfig):
    name = 'import_csv'


def handle_uploaded_file(f):
    csv_reader = csv.reader(f, dialect='excel')
    for row in csv_reader:
        print(', '.join(row))
