import csv

with open("data/training_data_all_ML.csv", 'w') as new_csv_file:
    csv_writer = csv.writer(new_csv_file)
    with open("data/training_data_android_gh_new.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            ranking = 0
            if line_count == 0:
                csv_writer.writerow(row)
            else:
                ML_code = int(row[3])
                ML_keyword = int(row[4])
                if ML_code > 0 or ML_keyword > 0:
                    csv_writer.writerow(row)
                print(row)
            line_count += 1
        print(f'Total {line_count} repos in travarsed')