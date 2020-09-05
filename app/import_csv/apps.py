from django.apps import AppConfig
import django.core.files.uploadhandler

import csv
import io


class ImportCsvConfig(AppConfig):
    name = 'import_csv'


def handle_uploaded_file(csv_file, file_content):
    file_content.update({'name': csv_file.name})
    file_content.update({'size': csv_file.size})

    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        file_content.update({'error1': 'This is not CSV file' })
        pass
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line
    # we are able to handle a data in a stream
    item_count = 1
    io_string = io.StringIO(data_set)
    next(io_string)
    file_content.update({'info': 'Here I am' })
    file_content.update({'string': io_string })
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        file_content.update({column[0]: column[1]})
        item_count = + 1

    file_content.update({'item count': item_count })


"""    with open(f.name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, dialect='excel')
        data_set = {'filename': csvfile.name}
        row_no = 0
        for row in csv_reader:
            row_no = + 1
            data_set.append({'Lp': row_no, 'object': row, })
"""
