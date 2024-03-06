import random


import pandas as pd
from sklearn.model_selection import train_test_split



trueList = [3722338, 7178062, 21728191, 50375733, 73989090, 89526065, 91033385, 96959404, 97069772, 104396349, 106363548, 111582650, 166464458, 179140820, 156573609, 4751]
falseList = [153739145, 142432236, 6068879, 38717234, 8941324, 11813432, 10980152, 13770782, 19701569, 56134258, 59398328, 64498659,
             137620200, 158403386, 172510805, 179115475, 72934873, 58651023, 100254459, 138721081, 70350765, 197733662,
             173143636, 46926847, 154598966, 81031065, 137676875, 1620146, 138274685, 205462662, 75316107, 10350623, 129525554, 61123937,
             105839540, 43732626, 40697069, 6665900, 7506289, 5682027, 87243781, 109117581, 63058347, 2398573, 3769055, 44428, 36425677,
             26245476, 66438665, 122255072, 51516315, 121660139, 105717457, 20985, 5866526]


def remove_initial_training_set(data_frame):
    for index, row in df.iterrows():
        repo_id = int(row['Repo_Id'])
        print(index, repo_id)
        if repo_id in trueList:
            df.drop(index, inplace=True)
        if repo_id in falseList:
            df.drop(index, inplace=True)
    return data_frame


def partition(lst, n):
    division = len(lst) / n
    return [lst[round(division * i):round(division * (i + 1))] for i in range(n)]

if __name__ == '__main__':
    df = pd.read_csv('data/merged_data_py_added.csv', low_memory=False)
    df = remove_initial_training_set(df)
    train_size = 0.8

    #X = df.drop(columns=['Is_Match']).copy()
    #y = df['Is_Match']

    #X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size)
    X_train, X_test = train_test_split(df, train_size=train_size)

    #test_size = 0.5
    #X_valid, X_test, y_valid, y_test = train_test_split(X_rem, y_rem, test_size=test_size)

    print(X_train.shape)#, print(y_train.shape)
    #print(X_valid.shape), print(y_valid.shape)
    print(X_test.shape)#, print(y_test.shape)

    X_train.to_csv('data/active_learning/training_data_all_rest.csv', index=False)
    #X_valid.to_csv('data/active_learning/validation_data.csv', index=False)
    X_test.to_csv('data/active_learning/test_data.csv', index=False)

    X_train = X_train.sample(frac=1).reset_index(drop=True)

    stages = partition(X_train, 40)
    for idx, stage in enumerate(stages):
        stage.to_csv('data/active_learning/stage_'+str(idx+1)+'.csv', index=True)

