from googleapiclient import discovery


from pymongo import MongoClient
import pandas
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client.git_projects
collection = db.C_sharp_projects

start_date = datetime(2019, 1, 1, 0, 0, 0)
archive_filter_count = 0
commit_filter_count = 0
desc_keyword_filter_count = 0
fork_filter_count = 0
language_filter_count = 0
LANG_API_KEY = 'AIzaSyCpIwsWdQ9v5Wvud2U-dluDz6BxOWwOSmA'
lang_client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=LANG_API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

negative_keywords = ['deprecated', 'obsolete', 'framework', 'library', 'testing', 'toolkit', 'example',
                     'sample', 'guideline', 'guide', 'tutorial', 'blog', 'book',
                     'libraries', 'toolchain', 'interview notes', 'curated collection']
                        # 'demo', 'demonstration',


def search_C_sharp_projects(csv_file):
    cursor = collection.find({'stargazers_count': {'$gt': 50}, 'updated_at': {'$gte': start_date}})
    mongo_docs = list(cursor)
    print("total docs:", len(mongo_docs))
    docs = pandas.DataFrame(columns=[])
    for num, doc in enumerate(mongo_docs):
        doc["_id"] = str(doc["_id"])
        doc_id = doc["_id"]
        keep = apply_filters(doc)
        if keep:
            series_obj = pandas.Series(doc, name=doc_id)
            docs = docs.append(series_obj)
    print(f'{archive_filter_count} docs filtered by archive')
    print(f'{commit_filter_count} docs filtered by commit date')
    print(f'{fork_filter_count} docs filtered by fork')
    print(f'{desc_keyword_filter_count} docs filtered by keywords')
    print(f'{language_filter_count} docs filtered by language')
    print("DataFrame len:", len(docs))
    docs.to_csv(csv_file, ",")
    csv_export = docs.to_csv(sep=",")


def apply_filters(project):
    if not filter_by_archive(project):
        global archive_filter_count
        archive_filter_count += 1
        return False
    if not filter_by_commit_date(project):
        global commit_filter_count
        commit_filter_count += 1
        return False
    if not filter_by_fork(project):
        global fork_filter_count
        fork_filter_count += 1
        return False
    if not filter_by_description(project):
        global desc_keyword_filter_count
        desc_keyword_filter_count += 1
        return False
    if not filter_by_language(project):
        global language_filter_count
        language_filter_count += 1
        return False
    return True


def filter_by_description(project):
    if not project["description"]:
        return True
    else:
        description = project["description"].lower()
        is_keyword_in_list = any(keyword in description for keyword in negative_keywords)
        return not is_keyword_in_list


def filter_by_archive(project):
    is_archived = project["archived"]
    return not is_archived


def filter_by_commit_date(project):
    if 'commits' in project:
        commit_data = project["commits"]
        for item in commit_data:
            try:
                last_commit_date = item["commit"]["committer"]["date"]
                datetime_commit = datetime.strptime(last_commit_date, "%Y-%m-%dT%H:%M:%SZ")
                if datetime_commit >= start_date:
                    return True
            except TypeError:
                return False
            break
    return False


def filter_by_fork(project):
    if project["description"]:
        description = project["description"].lower()
        if "forked from" in description or "fork of" in description:
            return False
    return True


def filter_by_language(project):
    if project["description"]:
        description = project["description"].lower()
        try:
            analyze_request = {
                'comment': {
                    'text': description},
                'requestedAttributes': {'TOXICITY': {}},
                'languages': ['en']
            }
            response = lang_client.comments().analyze(body=analyze_request).execute()
            languages = response['detectedLanguages']
            for lang in languages:
                if lang == 'en':
                    return True
        except Exception:
            print(f'Lang didnt work')
            return True
    print(f'Removing {project["id"]}: {project["full_name"]} due to Language')
    return False
