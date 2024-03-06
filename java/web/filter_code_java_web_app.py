import csv
import glob
import os
import sys
import pandas
from func_timeout import func_timeout, FunctionTimedOut
from pathlib import Path


java_gui_indicator = ['import org.springframework.', 'import javax.faces.bean.', 'import com.google.gwt.', 'import play.',
                       'import org.apache.struts2.', 'import com.opensymphony.xwork2.', 'import com.vaadin.',
                      'import org.apache.wicket.', 'import io.dropwizard.', 'import com.blade.',
                      'import grails.transaction.', 'import com.vogella.grails', 'jakarta.faces.application',
                      'import static spark.Spark.', 'import io.vertx.']
java_ext = '*.java'

pom_indicator = ['org.eclipse.jetty', 'com.opensymphony.xwork2', 'org.apache.struts2', 'io.dropwizard', 'com.bladejava',
                 'io.github.jhipster', 'com.sparkjava', 'org.apache.tapestry']
pom_ext = '*.xml'

def search_java_gui_indications(repo, app_indicator, ext):
    #try:
    #    files = func_timeout(5, glob.glob(repo+'**/'+ext, recursive=True))
    #except FunctionTimedOut:
    #    print(f'{repo} got timed out')
    #    files = []
    files = Path(repo).rglob(ext)
    #print(f'file count = {len(files)}')
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
            is_gui_app = False
            if line_count != 0:
                repo_id = row[2].replace(".0", "")
                print(f'Starting repo {repo_id}')
                if search_java_gui_indications(code_path + repo_id + "/", java_gui_indicator, java_ext):
                    is_gui_app = True
                    print(f'Got java UI in {repo_id}')
                if not is_gui_app:
                    if search_java_gui_indications(code_path + repo_id + "/", pom_indicator, pom_ext):
                        is_gui_app = True
                        print(f'Got xml UI in {repo_id}')
                if is_gui_app:
                    series_obj = pandas.Series(row, name=repo_id)
                    docs = docs.append(series_obj)
                    app_count += 1
                    print(f'Total {app_count} apps found so far in {line_count}.')
            line_count += 1
        docs.to_csv(java_app_csv_name, ",")
        docs.to_csv(sep=",")
        print(f'Total {app_count} apps found.')
