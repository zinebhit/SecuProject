import pandas as pd
from numba import njit, prange

from metrics import Metrics
from defense import Defense
from sacrificeHour import hour_sacrifice


if __name__ == '__main__':
    column_names = ["ID", "DateTime", "X", "Y"]
    dtypes = {'ID': 'str', 'DateTime': 'str', 'X': 'float64', 'Y': 'float64'}
    parse_dates = ['DateTime']
    df = pd.read_csv('entree.csv', sep='\t', header=None, names=column_names, dtype=dtypes, parse_dates=parse_dates)
    #df = pd.read_csv('smallBDD.csv', sep='\t', header=None, names=column_names, dtype=dtypes, parse_dates=parse_dates)
    #defense = Defense()
    #df_id_anonymized = defense.disturb_id(df)
    #print(df_id_anonymized)

    # test sacrificeHour
    df2 = df.copy()
    hour_sacrifice(df2, {"column": "DateTime", "params": (2, 100, 100)});
    metrics = Metrics(df2, df)
    metrics.calculate_all()
    # {"name": "sacrificeHour", "options": {"column": "date", "params": (2, 100, 100)}},
