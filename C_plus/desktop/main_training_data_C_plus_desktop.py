from C_plus import filtered_csv_generator_C_plus

if __name__ == '__main__':
    base_csv_path_C_plus = "data/filtered_C_plus.csv"
    readme_path = "/DATA/nadian/C_plus/readme/"
    code_path = "/DATA/nadian/C_plus/code/"
    C_plus_app_csv_path = "data/filtered_C_plus_desktop_app.csv"
    training_csv_path = "data/training_data_C_plus_desktop.csv"
    filtered_csv_generator_C_plus.search_C_plus_projects(base_csv_path_C_plus)
    #filter_code_java_desktop_app.filter_app(base_csv_path_java, code_path, java_app_csv_path)
    #data_generator_java_desktop.generate(java_app_csv_path, readme_path, code_path, training_csv_path)

