import data_generator_ios
import filter_code_ios_app
import filtered_csv_generator_ios

if __name__ == '__main__':
    base_csv_path_ios = "data/filtered_ios.csv"
    readme_path = "/DATA/nadian/ios/readme/"
    code_path = "/DATA/nadian/ios/code/"
    ios_app_csv_path = "data/filtered_ios_app.csv"
    training_csv_path = "data/training_data_ios.csv"
    filtered_csv_generator_ios.search_ios_projects(base_csv_path_ios)
    filter_code_ios_app.filter_app(base_csv_path_ios, code_path, ios_app_csv_path)
    data_generator_ios.generate(ios_app_csv_path, readme_path, code_path, training_csv_path)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
