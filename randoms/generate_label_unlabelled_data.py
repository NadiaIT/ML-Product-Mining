import csv
import json

projectList = []
trueList = []

with open('data/checked_project_list.txt') as f:
    projectList = f.readlines()
    f.close()
projectList = [s.strip() for s in projectList]

with open('data/positive_project_list') as f:
    trueList = f.readlines()
    f.close()
trueList = [s.strip() for s in trueList]

#with open("data/training_data_android_labelled.csv", 'w') as labeled_csv_file, open('data/training_data_android_unlabelled.csv', 'w') as unlabeled_csv_file:
with open("data/complete_training_data.csv", 'w') as complete_csv_file:

    #l_csv_writer = csv.writer(labeled_csv_file)
    #u_csv_writer = csv.writer(unlabeled_csv_file)
    csv_writer = csv.writer(complete_csv_file)
    with open("data/training_data_search_android_py_new_cols_added.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #u_csv_writer.writerow(row)
                row.append("Is_Match")
                #l_csv_writer.writerow(row)
                csv_writer.writerow(row)
                line_count += 1
            else:
                link = row[2].strip()
                print(link)
                print(row[11])
                row[11] = json.loads(row[11])
                print(row[11])
                row[11] = row[11][0]+row[11][1]
                print(row[11])
                if link in trueList:
                    row.append(True)
                    #l_csv_writer.writerow(row)
                    csv_writer.writerow(row)
                    line_count += 1
                elif link in projectList:
                    row.append(False)
                    #l_csv_writer.writerow(row)
                    csv_writer.writerow(row)
                    line_count += 1
                else:
                    #u_csv_writer.writerow(row)
                    row.append(False)
                    csv_writer.writerow(row)
                    line_count += 1
                #print(row)
        print(f'Total {line_count} repos in travarsed')