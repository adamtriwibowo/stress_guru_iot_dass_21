import pandas as pd

df = pd.read_excel('DATA PENELITIAN.xlsx', header=None)
print('All data (56 rows):')
print(df.to_string())
print('\n\nUnique values in each column:')
for i in range(df.shape[1]):
    print(f'\nColumn {i}: {df[i].unique()[:15]}')
