import pandas as pd

def hour_generalisation(x):
    if ((x.hour)>=6 and (x.hour)<11) :
        return (pd.datetime(x.year, x.month, x.day, 9 ,0,0))
    elif ((x.hour)>=11 and (x.hour)<14) :
        return (pd.datetime(x.year, x.month, x.day, 12 ,0,0))
    elif ((x.hour)>=14 and (x.hour)<18) :
        return (pd.datetime(x.year, x.month, x.day, 15 ,0,0))  
    elif ((x.hour)>=18 and (x.hour)<21) :
        return (pd.datetime(x.year, x.month, x.day, 20 ,0,0)) 
    else :
        return (pd.datetime(x.year, x.month, x.day, 2 ,0,0))    

def main(df, options):
    df.loc[:,options['column']] = df.loc[:,options['column']].apply(hour_generalisation)
    return df
  