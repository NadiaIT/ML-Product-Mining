import csv
import glob
import os
import sys
import pandas
from func_timeout import func_timeout, FunctionTimedOut
from pathlib import Path


C_sharp_gui_indicator = ['using Windows.UI.Xaml', 'using Windows.UI.', 'using System.Windows', 'using Uno.UI',
                         'using UIKit', 'Xamarin.Forms.Platform.iOS', 'using Xamarin.Forms',
                         'Xamarin.Forms.Platform.Android.', 'Xamarin.Forms.Forms', 'using Avalonia',
                         'UIWindow', 'UIApplicationDelegate', 'using Microsoft.AspNetCore.Identity.UI']
C_sharp_ext = '*.cs'

Xaml_gui_indicator = ['<Window', '<Page', '<Frame', '<Application', '<ContentPage']
Xaml_ext = '*.xaml'

def search_C_sharp_xamls(repo):
    files = list(Path(repo).rglob('*.xaml.cs'))
    files.extend(list(Path(repo).rglob('*.xaml.vb')))
    if len(files) > 0:
        return True
    return False


def search_C_sharp_gui_indications(repo, app_indicator, ext):
    #try:
    #    files = func_timeout(5, glob.glob(repo+'**/'+ext, recursive=True))
    #except FunctionTimedOut:
    #    print(f'{repo} got timed out')
    #    files = []
    files = list(Path(repo).rglob(ext))
    print(f'file count = {len(files)} for {ext}')
    for file in files:
        try:
            with open(file, 'r') as f:
                try:
                    lines = f.readlines()
                    print(f'Checking file - {file}.')
                    for line in lines:
                        if any(key in line for key in app_indicator):
                            print(f'Found in {line} in {file}')
                            return True
                except UnicodeDecodeError:
                    print(f'Got error reading file - {file}.')
        except FileNotFoundError:
            print(f'File not found - {file}.')
        except IsADirectoryError:
            print(f'{file} is a directory.')
    return False

def filter_app(csv_name, code_path, java_app_csv_name):
    csv.field_size_limit(sys.maxsize)
    docs = pandas.DataFrame(columns=[])
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        app_count = 0
        for row in csv_reader:
            got_UI_indication = False
            if line_count != 0:
                repo_id = row[2].replace(".0", "")
                print(f'Starting repo {repo_id}')
                if search_C_sharp_xamls(code_path + repo_id + "/"):
                    got_UI_indication = True
                    print(f'Got xaml.cs/xaml.vb in {repo_id}')
                if not got_UI_indication:
                    if search_C_sharp_gui_indications(code_path + repo_id + "/", Xaml_gui_indicator, Xaml_ext):
                        got_UI_indication = True
                        print(f'Got xaml UI in {repo_id}')
                if not got_UI_indication:
                    if search_C_sharp_gui_indications(code_path + repo_id + "/", C_sharp_gui_indicator, C_sharp_ext):
                        got_UI_indication = True
                        print(f'Got cs UI in {repo_id}')
                if got_UI_indication:
                    series_obj = pandas.Series(row, name=repo_id)
                    docs = docs.append(series_obj)
                    app_count += 1
                    print(f'Total {app_count} apps found so far in {line_count}.')
            line_count += 1
        docs.to_csv(java_app_csv_name, ",")
        docs.to_csv(sep=",")
        print(f'Total {app_count} apps found.')
