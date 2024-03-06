from android import filtered_csv_generator_android, data_generator_added_python_library, filter_code_android_app

if __name__ == '__main__':
    base_csv_path_android = "data/filtered_android_gh_final.csv"
    readme_path = "/DATA/nadian/android_gh/data/readme/"
    code_path = "/DATA/nadian/android_gh/new_code/"
    android_app_csv_path = "data/filtered_android_app_gh_final.csv"
    ranked_csv_path = "data/training_data_android_gh_new_py_added.csv"
    #ranked_csv_path = "data/training_data_all_ML.csv"
    filtered_csv_generator_android.search_android_projects(base_csv_path_android)
    filter_code_android_app.filter_app(base_csv_path_android, code_path, android_app_csv_path)
    #ranker.rank(android_app_crepo_idsv_path, readme_path, code_path, ranked_csv_path)
    #data_generator.generate(android_app_csv_path, readme_path, code_path, ranked_csv_path)
    data_generator_added_python_library.generate(android_app_csv_path, readme_path, code_path, ranked_csv_path)
    #linear_model.train(ranked_csv_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
