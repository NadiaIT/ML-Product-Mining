import data_generator_java_desktop
import filter_code_java_desktop_app
from java import filtered_csv_generator_java, remove_pom_maven_libraries

if __name__ == '__main__':
    base_csv_path_java = "data/filtered_java_corrected.csv"
    readme_path = "/DATA/nadian/java/readme/"
    code_path = "/DATA/nadian/java/code/"
    java_app_csv_path = "data/filtered_java_desktop_app_corrected.csv"
    training_csv_path = "data/training_data_java_desktop_corrected.csv"
    no_maven_training_csv_path = "data/training_data_java_desktop_no_maven.csv"
    filtered_csv_generator_java.search_java_projects(base_csv_path_java)
    filter_code_java_desktop_app.filter_app(base_csv_path_java, code_path, java_app_csv_path)
    data_generator_java_desktop.generate(java_app_csv_path, readme_path, code_path, training_csv_path)
    remove_pom_maven_libraries.filter_out_library(training_csv_path, code_path, no_maven_training_csv_path)

