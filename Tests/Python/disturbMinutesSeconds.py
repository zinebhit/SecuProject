import random
import pandas as pd


# Détection des POI -nuit, travail et weekend- durant les heures suivantes:
# night_start, night_end = 22, 6
# De 22h00 à 6h00
# work_start, work_end = 9, 16
# De 9h00 à 16h00
# weekend_start, weekend_end = 10, 18

def main(df, options):
    key1 = input("Please enter disturbMinutesSeconds' Key1: ")
    print("Key1 :",key1)
    key2 = input("Please enter disturbMinutesSeconds' Key2 : ")
    print("Key2 :",key2)
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : pd.datetime(x.year, x.month, x.day, x.hour,random.randint(0,int(key1)),random.randint(0,int(key2))))
    #df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : pd.datetime(x.year, x.month, x.day, x.hour,random.randint(0,59) ,random.randint(0,59) ))
    return df
