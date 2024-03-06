import csv
import sys
import pandas
from pathlib import Path


python_gui_indicator = ["from django.", "import django", "from masonite.", "import masonite", "from tg import", "import tg", "cubicweb", "web2py", "from dash import Dash", "django", "import grok", "from jam.wsgi import create_application", "from jam.wsgi_server import run", "from jam.", "from pylons", "from reahl.web.", "from websauna.", "from wheezy.", "zopeinstance", "from kiss.", "from lino", "from lino_book.", "import pylatte.web.", "from tipfy import", "import tornado.", "from tornado import", "from watson.framework import", "import webapp2", "webapp2.WSGIApplication(", "from web.core import Application", "serve(\'wsgiref\')", "import web", "web.application(", "from webware.Scripts.WebwareCLI import", "from Page import Page", "import webware", "from werkzeug.wrappers import", "@Request.application", "from werkzeug.serving import run_simple", "run_simple(", "import aiohttp", "aiohttp.ClientSession()", "WebSocketResponse(", "from bottle import", "from bottle import Bottle", "Bottle()", "import cherrypy", "@cherrypy.expose", "falcon.App()", "from wsgiref.simple_server import make_server", "import falcon", ".serve_forever()", "make_server(", "from fastapi import FastAPI", "FastAPI()", "from flask import Flask", "Flask(", "from flask import", "import hug", "@hug.get(", "rom pyramid.", "from wsgiref.", "from quart import Quart", "from quart_schema", "from quart", "QuartSchema(", "Quart(", "import bobo", "@bobo.query(", "from clastic import Application", "from clastic.", "from twisted.web import", "from twisted.", "from nevow import", "from sanic import Sanic", "from sanic.", "Sanic(", "from tornado.", "from chaussette", "from rocket import Rocket", "from spawning import", "from waitress import serve", "serve(", "from giotto.", "from albatross import", "from circuits import", "from circuits.", "from growler import App", "App()", "import growler", "growler.App(", "import morepath", "@App.path(", "from pycnic", "bluebream", "from quixote", "import muffin", "muffin.Application()", "import ray", "from vibora import Vibora", "from vibora.", "Vibora()"]
python_ext = '*.py', '*.ipynb'

config_gui_indicator = ["listen ", "web2py", "cubicweb", "django", "zopeinstance", "<pylatte-server>"]
config_ext = '*.conf', '*.ini', '*.xml', '*.web.config'

def search_python_gui_indications(repo, app_indicator, exts):
    #files = Path(repo).rglob(ext)
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
                if search_python_gui_indications(code_path + repo_id + "/", python_gui_indicator, python_ext):
                    is_gui_app = True
                    print(f'Got python UI in {repo_id}')
                if not is_gui_app:
                    if search_python_gui_indications(code_path + repo_id + "/", config_gui_indicator, config_ext):
                        is_gui_app = True
                        print(f'Got config UI in {repo_id}')
                if is_gui_app:
                    series_obj = pandas.Series(row, name=repo_id)
                    docs = docs.append(series_obj)
                    app_count += 1
                    print(f'Total {app_count} apps found so far in {line_count}.')
            line_count += 1
        docs.to_csv(python_app_csv_name, ",")
        docs.to_csv(sep=",")
        print(f'Total {app_count} apps found.')
