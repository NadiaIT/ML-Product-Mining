import csv

trueList = [3722338, 7178062, 21728191, 50375733, 73989090, 89526065, 91033385, 96959404, 97069772, 104396349, 106363548, 111582650, 166464458, 179140820, 156573609, 4751]
falseList = [153739145, 142432236, 6068879, 38717234, 8941324, 11813432, 10980152, 13770782, 19701569, 56134258, 59398328, 64498659,
             137620200, 158403386, 172510805, 179115475, 72934873, 58651023, 100254459, 138721081, 70350765, 197733662,
             173143636, 46926847, 154598966, 81031065, 137676875, 1620146, 138274685, 205462662, 75316107, 10350623, 129525554, 61123937,
             105839540, 43732626, 40697069, 6665900, 7506289, 5682027, 87243781, 109117581, 63058347, 2398573, 3769055, 44428, 36425677,
             26245476, 66438665, 122255072, 51516315, 121660139, 105717457, 20985, 5866526]

with open("data/training_data_selected.csv", 'w') as new_csv_file:
    csv_writer = csv.writer(new_csv_file)
    with open("data/training_data_android_gh_new.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                csv_writer.writerow(row)
                line_count += 1
            else:
                Repo_id = int(row[0])
                print(Repo_id)
                if Repo_id in trueList:
                    row[11] = True
                    csv_writer.writerow(row)
                    line_count += 1
                if Repo_id in falseList:
                    row[11] = False
                    csv_writer.writerow(row)
                    line_count += 1
                print(row)
        print(f'Total {line_count} repos in travarsed')