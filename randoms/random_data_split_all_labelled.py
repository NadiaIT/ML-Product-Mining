
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('data/final/complete_training_data.csv', low_memory=False)
#train_size = 0.8
dev_size = 0.67
cv_size = 0.7

X_cv, X_remain = train_test_split(df, train_size=cv_size)

X_dev, X_test = train_test_split(X_remain, train_size=dev_size)

print(X_cv.shape)
print(X_dev.shape)
print(X_test.shape)

X_cv.to_csv('data/final/cv_data.csv', index=False)
X_dev.to_csv('data/final/dev_data.csv', index=False)
X_test.to_csv('data/final/test_data.csv', index=False)