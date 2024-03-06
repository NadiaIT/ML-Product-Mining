import csv
import glob
import os
import sys
import pandas

app_indicator = 'com.android.application'
app_file_name = 'build.gradle*'


def search_android_app_indications(repo):
    for file in glob.glob(repo+'**/'+app_file_name, recursive=True):
        try:
            with open(file, 'r') as f:
                try:
                    lines = f.readlines()
                    print(f'Checking file - {file}.')
                    for line in lines:
                        if app_indicator in line:
                            print(f'Found in {line}')
                            return True
                except UnicodeDecodeError:
                    print(f'Got error reading file - {file}.')
        except FileNotFoundError:
            print(f'File not found - {file}.')
    return False


def filter_app(csv_name, code_path, android_app_csv_name):
    csv.field_size_limit(sys.maxsize)
    docs = pandas.DataFrame(columns=[])
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        app_count = 0
        for row in csv_reader:
            if line_count != 0:
                repo_id = row[2].replace(".0", "")
                is_app = search_android_app_indications(code_path + repo_id + "/")
                if is_app:
                    series_obj = pandas.Series(row, name=repo_id)
                    docs = docs.append(series_obj)
                    app_count += 1
                    print(f'Total {app_count} apps found so far in {line_count}.')
            line_count += 1
        docs.to_csv(android_app_csv_name, ",")
        docs.to_csv(sep=",")
        print(f'Total {app_count} apps found.')
