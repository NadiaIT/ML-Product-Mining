import csv
import sys
import pandas
from pathlib import Path


python_gui_indicator = ['from PyQt5 import QtWidgets', 'from PyQt5.QtWidgets import Qwidget',
    'import PyQt5', 'from PyQt5.QtGui', 'from PyQt5.QtCore', 'import tkinter', 'from tkinter import',
    'from kivy.app import', 'from kivy.uix.* import', 'import kivy', 'import wx',
    'from wxPython.wx import', 'from libavg import', 'import libavg', 'import PySimpleGUI',
    'from PySimpleGUI importcd', 'import pyforms', 'from pyforms.basewidget import',
    'from pyforms.controls import', 'from pyforms import', 'from wax import', 'from wax.tools.* import',
    'import wx', 'from dearpygui.core import', 'from dearpygui.simple import', 'import dearpygui.dearpygui',
    'from PySide2.QtWidgets import', 'from PySide2.QtCore', 'import PySide2',
    'from pywinauto.application import', 'import pywinauto', 'import remi.gui', 'from remi import',
    'from PyQt6.QtWidgets import', 'from PyQt4 import', 'from PyQt6.QtCore import', 'from PyQt6 import',
    'from PyQt6.QtGui import', 'from PySide6.QtUiTools import', 'from PySide6 import']
python_ext = '*.py'


def search_python_gui_indications(repo, app_indicator, ext):
    files = Path(repo).rglob(ext)
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


def filter_app(csv_name, code_path, python_app_csv_name):
    csv.field_size_limit(sys.maxsize)
    docs = pandas.DataFrame(columns=[])
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        app_count = 0
        for row in csv_reader:
            if line_count != 0:
                repo_id = row[2].replace(".0", "")
                print(f'Starting repo {repo_id}')
                is_gui_app = search_python_gui_indications(code_path + repo_id + "/", python_gui_indicator, python_ext)
                if is_gui_app:
                    series_obj = pandas.Series(row, name=repo_id)
                    docs = docs.append(series_obj)
                    app_count += 1
                    print(f'Total {app_count} apps found so far in {line_count}.')
            line_count += 1
        docs.to_csv(python_app_csv_name, ",")
        docs.to_csv(sep=",")
        print(f'Total {app_count} apps found.')
