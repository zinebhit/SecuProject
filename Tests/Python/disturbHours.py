import random
import pandas as pd

def main(df, options):
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : pd.datetime(x.year, x.month, x.day, random.randint(0,23),x.minute,x.second ))
    return df