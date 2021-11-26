import random
import pandas as pd


#Change ids with random value for a whole interval that doesn't exceed the week limitation


def main(df, options):
    column = options["column"]
    df["week"]=df['date'].dt.isocalendar().week 
    print(df['id'].unique())
    ids=df['id'].unique()
    Weeks =df["week"].unique()
    
    for i in ids :
         for week in Weeks :
    
            df.loc[(df['week']==week) &(df['id']==i),'id']= random.choice(ids)

    del df["week"]
    return df


