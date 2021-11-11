import pandas as pd


from metrics import Metrics


if __name__ == '__main__':
    column_names = ["ID", "DateTime", "X", "Y"]
    dtypes = {'ID': 'int64', 'DateTime': 'str', 'X': 'float64', 'Y': 'float64'}
    parse_dates = ['DateTime']
    # df = pd.read_csv('data_set.csv', sep='\t', header=None, names=column_names, dtype=dtypes, parse_dates=parse_dates)
    df = pd.read_csv('smallBDD.csv', sep='\t', header=None, names=column_names, dtype=dtypes, parse_dates=parse_dates)
    metrics = Metrics(df, df)
    metrics.calculate_all()