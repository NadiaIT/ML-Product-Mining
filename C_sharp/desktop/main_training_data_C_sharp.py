import data_generator_C_sharp_desktop
from C_sharp import filtered_csv_generator_C_sharp
from C_sharp.desktop import filter_code_C_sharp_desktop_app

if __name__ == '__main__':
    base_csv_path_C_sharp = "data/filtered_C_sharp.csv"
    readme_path = "/DATA/nadian/C_sharp/readme/"
    code_path = "/DATA/nadian/C_sharp/code/"
    C_sharp_app_csv_path = "data/filtered_C_sharp_desktop_app.csv"
    training_csv_path = "data/training_data_C_sharp_desktop.csv"
    filtered_csv_generator_C_sharp.search_C_sharp_projects(base_csv_path_C_sharp)
    filter_code_C_sharp_desktop_app.filter_app(base_csv_path_C_sharp, code_path, C_sharp_app_csv_path)
    data_generator_C_sharp_desktop.generate(C_sharp_app_csv_path, readme_path, code_path, training_csv_path)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
