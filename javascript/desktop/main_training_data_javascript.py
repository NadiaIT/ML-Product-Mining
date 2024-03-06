import filtered_csv_generator_javascipt
import filter_code_javascript_desktop_app
import data_generator_javascript_desktop

if __name__ == '__main__':
    base_csv_path_javascript = "data/filtered_javascript_1.csv"
    readme_path = "/DATA/nadian/javascript/readme/"
    code_path = "/DATA/nadian/javascript/code/"
    javascript_app_csv_path = "data/filtered_javascript_desktop_app_1.csv"
    training_csv_path = "data/training_data_javascript_desktop_1.csv"
    #filtered_csv_generator_javascipt.search_javascript_projects(base_csv_path_java)
    #filter_code_javascript_desktop_app.filter_app(base_csv_path_javascript, code_path, javascript_app_csv_path)
    data_generator_javascript_desktop.generate(javascript_app_csv_path, readme_path, code_path, training_csv_path)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
