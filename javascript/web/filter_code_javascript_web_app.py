import csv
import sys
import pandas
from pathlib import Path


js_gui_indicator = ['require("express")', 'require(\'express\')', 'express()', 'require("@hapi/hapi")',
                    'require(\'@hapi/hapi\')', 'from \'actionhero\'', 'from "actionhero"',
                    'require(\'restify\')', 'require("restify")', 'require(\'sails\')', 'require("sails"")',
                    'from \'@loopback/', 'from "@loopback/', 'require(\'@feathersjs/', 'require(\'total4/'
                    'require(\'koa\')', 'require("koa")', 'new Koa()', '@adonisjs/lucid/providers/'
                    'require("@feathersjs/', 'require("total4/', 'require("moleculer")', 'require(\'moleculer\')',
                    'require(\'fastify\')', 'require("fastify")', 'import Fastify', 'Deno.listen(', 'Deno',
                    ' require("http")', ' require(\'http\')', 'from \'meteor/http\'', 'from "meteor/http"',
                    'NestFactory', 'from \'@nestjs/', 'from "@nestjs/',
                    '.listen(', '.server(', '.createServer()', 'await app.listen(']
js_ext = '*.js', '*.ts', '*.jsx', '*.jsp', '*.html', '*.htm'

json_gui_indicator = ['"actionhero":', '"start": "fastify start ', '"start": "next start"', 
                      '"start": "nuxt start"']
json_ext = 'package.json', 'this is dummy just to check'


def search_javascript_gui_indications(repo, app_indicator, exts):
    files = []
    for ext in exts:
        print(f'ext={ext}')
        files.extend(Path(repo).rglob(ext))
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
            is_gui_app = False
            if line_count != 0:
                repo_id = row[2].replace(".0", "")
                print(f'Starting repo {repo_id}')
                if search_javascript_gui_indications(code_path + repo_id + "/", json_gui_indicator, json_ext):
                    is_gui_app = True
                    print(f'Got java UI in {repo_id}')
                if not is_gui_app:
                    if search_javascript_gui_indications(code_path + repo_id + "/", js_gui_indicator, js_ext):
                        is_gui_app = True
                        print(f'Got xml UI in {repo_id}')
                if is_gui_app:
                    series_obj = pandas.Series(row, name=repo_id)
                    docs = docs.append(series_obj)
                    app_count += 1
                    print(f'Total {app_count} apps found so far in {line_count}.')
            line_count += 1
        docs.to_csv(python_app_csv_name, ",")
        docs.to_csv(sep=",")
        print(f'Total {app_count} apps found.')
