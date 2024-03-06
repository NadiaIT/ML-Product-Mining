import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


def train(training_data):
    raw_data = pd.read_csv(training_data)
    raw_data.info()
    #sns.pairplot(raw_data)
    #plt.show()
    x = raw_data[['Code_ML_Library_Occurance', 'General_ML_Keyword_Occurance',
                  'Apk_Mention_Count', 'Apk_Link_Count', 'Has_Valid_Homepage',
                  'Commit_Count', 'Release_Count', 'Contributor_Count']]
    y = raw_data['Is_Match']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    model = LinearRegression()
    model.fit(x_train, y_train)
    print(model.coef_)
    print(model.intercept_)
    predictions = model.predict(x_test)
    plt.scatter(y_test, predictions)
    #plt.show()
    plt.hist(y_test - predictions)
    #plt.show()


