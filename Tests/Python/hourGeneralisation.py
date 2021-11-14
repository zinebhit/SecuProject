import pandas as pd
from random import *

def hour_generalisation(x):
    if ((x.hour)>=6 and (x.hour)<11) :
        return (pd.datetime(x.year, x.month, x.day, 9 ,randint(0,59),randint(0,59)))
    elif ((x.hour)>=11 and (x.hour)<14) :
        return (pd.datetime(x.year, x.month, x.day, 12 ,randint(0,59),randint(0,59)))
    elif ((x.hour)>=14 and (x.hour)<18) :
        return (pd.datetime(x.year, x.month, x.day, 15 ,randint(0,59),randint(0,59)))  
    elif ((x.hour)>=18 and (x.hour)<21) :
        return (pd.datetime(x.year, x.month, x.day, 20 ,randint(0,59),randint(0,59))) 
    else :
        return (pd.datetime(x.year, x.month, x.day, 2 ,randint(0,59),randint(0,59)))    

def f(x):
    i = randint(1,1000)
    if (i == 500): return (pd.datetime(x.year, x.month, x.day, randint(0,23) ,randint(0,59),randint(0,59)))
    hour_generalisation(x)

def main(df, options):
    df.loc[:,options['column']] = df.loc[:,options['column']].apply(lambda x: f(x))
    return df
  