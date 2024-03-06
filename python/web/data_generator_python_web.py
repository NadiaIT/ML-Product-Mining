import glob, os
import csv
import sys
from pathlib import Path
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('localhost', 27017, username='nadia', password='cmu@242')
db = client.git_projects

collection = db.python_projects
apk_mentions = ['website ', 'deployed', 'visit', 'web application', 'browser', 'google chrome', 'internet explorer',
                'firefox', 'opera', 'microsoft edge']
apk_link = ['www.', 'http://', 'https://' '.com', '.org', '.edu']
ML_library_keyword = ['weka.', 'tensorflow', 'import numpy', 'from numpy', 'from scipy', 'import scipy',
                      'from sklearn', 'import sklearn', 'import theano', 'from theano', 'from torch',
                      'import torch', 'import pandas', 'from pandas', 'from matplotlib',  'import mlpack',
                      'import matplotlib', 'from mlpack', 'import nltk', 'from nltk', 'from scrapy',
                      'from bs4 import BeautifulSoup', 'import scrapy', 'from seaborn', 'import pycaret',
                      'import seaborn', 'from pycaret', 'from caffe', 'import shogun', 'from daal4py',
                      'import caffe', 'import chainer', 'from chainer', 'from shogun', 'import daal4py',
                      'import dlib', 'from dlib', 'from cv2', 'import cv2', 'from sparkdl', 'import sparkdl',
                      'from pyspark.ml', 'import mxnet', 'import pyspark.ml', 'from dask', 'from datatable',
                      'from mxnet', 'import dask', 'import datatable', 'import pyspark.mllib', 'from plotly',
                      'from pyspark.mllib', 'import plotly', 'from Orange', 'import Orange', 'import statsmodels',
                      'from bokeh', 'import eli5', 'import xgboost', 'import spacy', 'import gensim',
                      'from gensim', 'import lightgbm', 'from catboost', 'from fastai', 'import gluonnlp',
                      'from statsmodels', 'import bokeh', 'from eli5', 'from xgboost', 'from spacy',
                      'from lightgbm', 'import catboost', 'import fastai', 'from gluonnlp',
                      'com.google.firebase.ml', 'com.google.mlkit', 'bigml.com', 'bigml.io']
ML_library_keyword_py = ['orange3', 'DiffSharp', 'opennn', 'dynet', 'fann', 'armadillo',
                         'Vulpes', 'Deedle', 'FSharp', 'm2cgen', 'opencv']
code_extensions = ['.py', '.ipynb', '.json', '.xml']
ML_general_keyword = ['machine learning', 'artificial intelligent', 'artificial intelligence', ' ml ', ' ai ', '//ml ', '//ai ']
general_extensions = ['.md', '.txt', '.json', '.xml', 'xaml']
homepage_filters = ['github.com', 'gitlab.com']

model_extensions = ['.pb', '.pkl', '.pmml', '.pt', '.mlmodel', '.onnx', '.tflite', '.tfrecords']
other_ML_entensions = ['.h5', '.petastorm', '.parquet', '.npy', '.orc', '.avro']

common_ML_applications = ['ocr', 'tts', 'stt', 'nlp', 'cnn', 'classification', 'image processing', 'face detection',
                          'object detection', 'recognition', 'prediction', 'forecast', 'svm', 'lstm', 'scanner']

def get_files(repo, extensions):
    all_files = []
    for ext in extensions:
        all_files.extend(Path(repo).rglob('*' + ext))
    return all_files


def search_ML_library_in_repository(repo):
    ML_lib_count = 0
    ML_key_count = 0
    ML_app_count = 0
    files = get_files(repo, code_extensions)
    for file in files:
        try:
            with open(file, 'r') as f:
                try:
                    lines = f.readlines()
                    for line in lines:
                        is_library_in_list = any(keyword in line.lower() for keyword in ML_library_keyword)
                        if is_library_in_list:
                            ML_lib_count += 1
                            print(f'Found ML library in {file}.')
                        is_py_library_in_list = any(keyword in line.lower() for keyword in ML_library_keyword_py)
                        if is_py_library_in_list:
                            ML_lib_count += 1
                            print(f'Found ML library in PY {file}.')
                        is_keyword_in_list = any(keyword in line.lower() for keyword in ML_general_keyword)
                        if is_keyword_in_list:
                            ML_key_count += 1
                            print(f'Found ML key in {file}.')
                        is_app_domain_in_list = any(keyword in line.lower() for keyword in common_ML_applications)
                        if is_app_domain_in_list:
                            ML_app_count += 1
                            print(f'Found ML app domain in {file}.')
                except UnicodeDecodeError as e:
                    print(f'Got error reading file - {file}.')
                    print(e)
        except Exception as e:
            print(e)
            print(f'File open issue - {file}.')
    return [ML_lib_count, ML_key_count, ML_app_count]


def search_ML_keyword_in_repository(repo):
    ML_key_count = 0
    files = get_files(repo, general_extensions)
    for file in files:
        try:
            with open(file, 'r') as f:
                try:
                    lines = f.readlines()
                    for line in lines:
                        is_keyword_in_list = any(keyword in line.lower() for keyword in ML_general_keyword)
                        if is_keyword_in_list:
                            ML_key_count += 1
                            print(f'Found ML general in {file}.')
                except UnicodeDecodeError:
                    print(f'Got error reading file - {file}.')
        except Exception:
            print(f'File open issue - {file}.')
    return ML_key_count


def search_apk_in_readme(readme):
    apk_link_count = 0
    apk_mention_count = 0
    try:
        with open(readme, 'r') as f:
            try:
                lines = f.readlines()
                for line in lines:
                    is_apk_in_line = any(apk in line.lower() for apk in apk_mentions)
                    if is_apk_in_line:
                        apk_mention_count += 1
                        print(f'Found apk mention in {readme}.')
                    is_link_in_line = any(apk in line.lower() for apk in apk_link)
                    if is_link_in_line:
                        apk_link_count += 1
                        print(f'Found apk link in {readme}.')
                return [apk_mention_count, apk_link_count]
            except Exception:
                print(f'Got error on {readme}')
                return [apk_mention_count, apk_link_count]
    except Exception:
        print(f'Got error opening {readme}')
        return [apk_mention_count, apk_link_count]


def find_valid_homepage(website):
    if not website:
        return False
    is_website_not_valid = any(page in website for page in homepage_filters)
    if is_website_not_valid:
        return False
    else:
        return True

def find_ML_extention(repo):
    model_files = get_files(repo, model_extensions)
    model_ext = 0
    other_ML_ext = 0
    for file in model_files:
        print(f'Found model file: {file}')
        model_ext += 1
    other_files = get_files(repo, other_ML_entensions)
    for file in other_files:
        print(f'Found other ml related file: {file}')
        other_ML_ext += 1
    return [model_ext, other_ML_ext]


def find_json_count(json_array):
    return len(json_array)


def generate(csv_name, readme_path, code_path, ranked_csv):
    csv.field_size_limit(sys.maxsize)
    csv_fields = ['Repo_Id', 'Name', 'Link', 'Code_ML_Library_Occurance', 'General_ML_Keyword_Occurance',
                  'Apk_Mention_Count', 'Apk_Link_Count', 'Has_Valid_Homepage', 'Commit_Count',
                  'Tag_Count', 'Committer_Count', 'Extension_Count', 'ML_Domain_Count']#, 'Is_Match']
    with open(ranked_csv, 'w') as new_csv_file:
        csv_writer = csv.writer(new_csv_file)
        csv_writer.writerow(csv_fields)
        with open(csv_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                ranking = 0
                if line_count != 0:
                    new_row = []
                    #row_id = int(row[1])
                    row_id = row[1]
                    #cursor = collection.find_one({"_id": ObjectId(row_id)})
                    #cursor = collection.find_one({"_id": row_id})
                    repo_id = row[3].replace(".0", "")
                    cursor = collection.find_one({"id": int(repo_id)})
                    print(f'Starting {row_id}: {repo_id}...')
                    new_row.append(repo_id)
                    new_row.append(cursor['full_name'])
                    new_row.append(cursor['html_url'])
                    lib_count = search_ML_library_in_repository(code_path + repo_id + "/")
                    new_row.append(lib_count[0])
                    new_row.append(search_ML_keyword_in_repository(code_path + repo_id + "/")+lib_count[1])
                    readme = readme_path + repo_id + ".md"
                    readme_apk_counts = search_apk_in_readme(readme)
                    new_row.append(readme_apk_counts[0])
                    new_row.append(readme_apk_counts[1])
                    new_row.append(find_valid_homepage(cursor['homepage']))
                    new_row.append(cursor['commit_count'])
                    new_row.append(cursor['tag_count'])
                    new_row.append(cursor['committer_count'])
                    new_row.append(find_ML_extention(code_path + repo_id + "/"))
                    new_row.append(lib_count[2])
                    #new_row.append(find_json_count(cursor['commits']))
                    #new_row.append(find_json_count(cursor['releases']))
                    #new_row.append(find_json_count(cursor['contributors']))
                    #new_row.append(False)
                    csv_writer.writerow(new_row)
                    print(new_row)
                line_count += 1
            print(f'Total {line_count} repos in travarsed')
