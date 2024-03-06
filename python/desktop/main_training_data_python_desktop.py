import filtered_csv_generator_python
import filter_code_python_desktop_app
import data_generator_python_desktop

if __name__ == '__main__':
    base_csv_path_python = "data/filtered_python_1.csv"
    readme_path = "/DATA/nadian/python/readme/"
    code_path = "/DATA/nadian/python/code/"
    python_app_csv_path = "data/filtered_python_desktop_app.csv"
    training_csv_path = "data/training_data_python_desktop.csv"
    #filtered_csv_generator_python.search_python_projects(base_csv_path_python)
    #filter_code_python_desktop_app.filter_app(base_csv_path_python, code_path, python_app_csv_path)
    data_generator_python_desktop.generate(python_app_csv_path, readme_path, code_path, training_csv_path)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
