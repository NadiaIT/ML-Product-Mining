import glob, os
import csv
import sys
from pathlib import Path
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('localhost', 27017)
db = client.git_projects
#collection = db.project_meta
collection = db.android_projects
apk_mentions = [' apk ', '.apk', 'playstore' 'play store']
apk_link = ['play.google.com', 'f-droid.org', 'www.coolapk.com']
ML_library_keyword = ['weka.', 'net.sf.javaml', 'org.apache.mahout', 'org.apache.spark',
                      'org.deeplearning4j', 'cc.mallet', 'tensorflow', 'edu.stanford.nlp',
                      'com.londogard.smile', 'smile.', 'nd4j']
ML_library_keyword_py = ['numpy', 'scipy', 'sklearn', 'theano', 'mlpack', 'seaborn', 'orange3'
                         'torch', 'pandas', 'keras', 'matplotlib', 'plotly', 'nltk']
code_extensions = ['.py', '.java', '.ipynb', '.cpp', '.c', '.h', '.hpp', '.ss', '.json', '.kt', '.dart']
ML_general_keyword = ['machine learning', 'artificial intelligent', 'artificial intelligence', ' ml ', ' ai ', '//ml ', '//ai ']
general_extensions = ['.md', '.txt', '.json', '.xml']
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
                    cursor = collection.find_one({"_id": ObjectId(row_id)})
                    #cursor = collection.find_one({"_id": row_id})
                    repo_id = row[3].replace(".0", "")
                    new_row.append(repo_id)
                    new_row.append(cursor['full_name'])
                    new_row.append(cursor['html_url'])
                    print(f'Starting {repo_id}...')
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
