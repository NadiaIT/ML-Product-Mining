import glob, os
import csv
import sys

apk_mentions = [' apk ', '.apk', 'playstore' 'play store']
apk_link = ['play.google.com', 'f-droid.org', 'www.coolapk.com']
ML_library_keyword = ['weka.', 'net.sf.javaml', 'org.apache.mahout', 'org.apache.spark',
                      'org.deeplearning4j', 'cc.mallet', 'tensorflow']
code_extensions = ['.py', '.java', '.ipynb', '.cpp', '.c', '.h', '.hpp', '.ss', '.json']
ML_general_keyword = ['machine learning', 'artificial intelligent', 'artificial intelligence', ' ml ', ' ai ']
general_extensions = ['.md', '.txt', '.json', '.xml']
homepage_filters = ['github.com', 'gitlab.com']


def search_keyword_in_repository(repo):
    code_rank = 0
    for root, dirs, files in os.walk(repo):
        for file in files:
            if file.endswith(tuple(code_extensions)):
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        try:
                            lines = f.readlines()
                            #print(f'Checking file - {os.path.join(root, file)}.')
                            for line in lines:
                                is_keyword_in_list = any(keyword in line.lower() for keyword in ML_library_keyword)
                                if is_keyword_in_list:
                                    code_rank += 10
                                    print(f'Found ML library in {file}.')
                        except UnicodeDecodeError:
                            print(f'Got error reading file - {os.path.join(root, file)}.')
                except FileNotFoundError:
                    print(f'File not found - {os.path.join(root, file)}.')
            elif file.endswith(tuple(general_extensions)):
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        try:
                            lines = f.readlines()
                            #print(f'Checking file - {os.path.join(root, file)}.')
                            for line in lines:
                                is_keyword_in_list = any(keyword in line.lower() for keyword in ML_general_keyword)
                                if is_keyword_in_list:
                                    code_rank += 5
                                    print(f'Found ML general in {file}.')
                        except UnicodeDecodeError:
                            print(f'Got error reading file - {os.path.join(root, file)}.')
                except FileNotFoundError:
                    print(f'File not found - {os.path.join(root, file)}.')
    return code_rank


def rank_by_readme(readme):
    readme_rank = 0
    try:
        with open(readme, 'r') as f:
            try:
                lines = f.readlines()
                for line in lines:
                    is_apk_in_line = any(apk in line.lower() for apk in apk_mentions)
                    if is_apk_in_line:
                        readme_rank += 5
                        print(f'Found apk mention in {readme}.')
                    is_link_in_line = any(apk in line.lower() for apk in apk_link)
                    if is_link_in_line:
                        readme_rank += 10
                        print(f'Found apk link in {readme}.')
                return readme_rank
            except Exception:
                print(f'Got error on {readme}')
                return readme_rank
    except Exception:
        print(f'Got error opening {readme}')
        return readme_rank


def rank_by_homepage(project):
    website = project[7]
    if not website:
        return 0
    is_website_not_valid = any(page in website for page in homepage_filters)
    if is_website_not_valid:
        return 0
    else:
        return 15


def rank(csv_name, readme_path, code_path, ranked_csv):
    csv.field_size_limit(sys.maxsize)
    total_ranked = 0
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            ranking = 0
            if line_count != 0:
                repo_id = row[2].replace(".0", "")
                ranking += search_keyword_in_repository(code_path + repo_id + "/")
                if ranking > 0:
                    readme = readme_path + repo_id + ".md"
                    ranking += rank_by_readme(readme)
                    ranking += rank_by_homepage(row)
            line_count += 1
            if ranking != 0:
                total_ranked += 1
                print(f'Rank of {repo_id} is {ranking}.')
        print(f'Total {total_ranked} repos in ranking')
