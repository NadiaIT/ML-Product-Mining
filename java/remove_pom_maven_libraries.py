import csv
import glob
import os
import sys
import pandas
from xml.etree import ElementTree as et
import requests
from pathlib import Path


app_file_name = 'pom.xml'
ns = "http://maven.apache.org/POM/4.0.0"


def search_maven_using_pom(repo):
    print(f'{repo}')
    files = Path(repo).rglob(app_file_name)
    # print(f'file count = {len(files)}')
    for file in files:
        try:
            group = artifact = version = ""
            tree = et.ElementTree()
            tree.parse(file)
            p = tree.getroot().find("{%s}parent" % ns)

            if p is not None:
                if p.find("{%s}groupId" % ns) is not None:
                    group = p.find("{%s}groupId" % ns).text

                if p.find("{%s}version" % ns) is not None:
                    version = p.find("{%s}version" % ns).text

            if tree.getroot().find("{%s}groupId" % ns) is not None:
                group = tree.getroot().find("{%s}groupId" % ns).text

            if tree.getroot().find("{%s}artifactId" % ns) is not None:
                artifact = tree.getroot().find("{%s}artifactId" % ns).text

            if tree.getroot().find("{%s}version" % ns) is not None:
                version = tree.getroot().find("{%s}version" % ns).text

            print(f'mvn:{group}, {artifact}, {version}')
            url = 'https://mvnrepository.com/artifact/'+group+"/"+artifact
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            result = requests.get(url, headers=headers)
            print(f'Status: {result.status_code}')
            if result.status_code == 404:
                return False
            else:
                return True
        except Exception:
            print(f'Got error in {file}.')
            return False
    return False


def filter_out_library(csv_name, code_path, new_csv_name):
    csv.field_size_limit(sys.maxsize)
    docs = pandas.DataFrame(columns=[])
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        app_count = 0
        for row in csv_reader:
            if line_count != 0:
                repo_id = row[0]
                is_library = search_maven_using_pom(code_path + repo_id + "/")
                if is_library:
                    print(f'Removing {repo_id} as found in maven...')
                else:
                    series_obj = pandas.Series(row, name=repo_id)
                    docs = docs.append(series_obj)
                    app_count += 1
            line_count += 1
        docs.to_csv(new_csv_name, ",")
        docs.to_csv(sep=",")
        print(f'Total {app_count} apps found.')




