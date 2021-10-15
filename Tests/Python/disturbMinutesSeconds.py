import random
import pandas as pd


def main(df, options):
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : pd.datetime(x.year, x.month, x.day, x.hour,random.randint(0,59) ,random.randint(0,59) ))
    return df
