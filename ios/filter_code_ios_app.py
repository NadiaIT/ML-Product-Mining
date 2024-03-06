import csv
import glob
import os
import sys
import pandas

swift_app_indicator = ['import SwiftUI', 'import UIKit']
objectiveC_app_indicator = ['#import <UIKit/UIKit.h>', '#import "AppDelegate.h"']
swift_ext = '*.swift'
objectiveC_ext = '*.m'


def search_ios_app_indications(repo, app_indicator, ext):
    for file in glob.glob(repo+'**/'+ext, recursive=True):
        try:
            with open(file, 'r') as f:
                try:
                    lines = f.readlines()
                    print(f'Checking file - {file}.')
                    for line in lines:
                        if any(key in line for key in app_indicator):
                            print(f'Found in {line}')
                            return True
                except UnicodeDecodeError:
                    print(f'Got error reading file - {file}.')
        except FileNotFoundError:
            print(f'File not found - {file}.')
        except IsADirectoryError:
            print(f'{file} is a directory.')
    return False


def filter_app(csv_name, code_path, ios_app_csv_name):
    csv.field_size_limit(sys.maxsize)
    docs = pandas.DataFrame(columns=[])
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        app_count = 0
        for row in csv_reader:
            if line_count != 0:
                repo_id = row[2].replace(".0", "")
                is_swift_app = search_ios_app_indications(code_path + repo_id + "/", swift_app_indicator, swift_ext)
                if not is_swift_app:
                    is_objectiveC_app = search_ios_app_indications(code_path + repo_id + "/", objectiveC_app_indicator, objectiveC_ext)
                if is_swift_app or is_objectiveC_app:
                    series_obj = pandas.Series(row, name=repo_id)
                    docs = docs.append(series_obj)
                    app_count += 1
                    print(f'Total {app_count} apps found so far in {line_count}.')
            line_count += 1
        docs.to_csv(ios_app_csv_name, ",")
        docs.to_csv(sep=",")
        print(f'Total {app_count} apps found.')
