import pandas as pd

ghtorrent = pd.read_csv("data/training_data_android_gh_new_py_added.csv")

git_api_search = pd.read_csv("data/training_data_search_android_py_added.csv")
all_projects = pd.concat([ghtorrent, git_api_search]).drop_duplicates(subset=['Link']).reset_index(drop=True)
print(all_projects.shape)
unique_projects = all_projects.drop_duplicates(subset=['Link']).reset_index(drop=True)
unique_projects.to_csv('data/merged_data_py_added.csv', index=False)
