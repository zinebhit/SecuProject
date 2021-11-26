from random import randint
import pandas as pd
# pd.options.mode.chained_assignment = None

unique = {}
uniques = []
seen = []

def main():
    unique = {}
    uniques = []
    seen = []
    size = 2
    column_names = ["ID", "DateTime", "X", "Y"]
    dtypes = {'ID': 'str', 'DateTime': 'str', 'X': 'float64', 'Y': 'float64'}
    parse_dates = ['DateTime']
    df = pd.read_csv('/Users/christinekhalil/Developer/SecuProject/Tests/Python/smallBDD.csv', sep='\t', header=None, names=column_names, dtype=dtypes, parse_dates=parse_dates)
    df_orig = df.copy()
    # Converting longitude and latitude as float 
    df = df.astype({'X': 'float64', 'Y': 'float64', 'ID': 'int64' })

    # Round lat,long with size
    df['X'] = df['X'].round(size)
    df['Y'] = df['Y'].round(size)

    # Group each position for ids and retrieve the count of unique position
    df = df.groupby(['ID','X','Y']).size().reset_index(name='count')
    df1 = df.loc[lambda df:df['count'] == 1]

    for row in df1.iterrows():
        uniques.append(row[0])

    return uniques

print(main())