import pandas as pd
import matplotlib.pyplot as plt

numbers = pd.read_csv('numbers.csv')

cumval=0
fig = plt.figure(figsize=(12,8))
for col in numbers.columns[~numbers.columns.isin(['index','category', 'augmented'])]:
    plt.bar(numbers.category, numbers[col], bottom=cumval, label=col)
    cumval = cumval+numbers[col]

_ = plt.xticks(rotation=30)
_ = plt.legend(fontsize=18)

plt.show()