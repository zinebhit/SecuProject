from random import *
import pandas as pd
import numpy as np

def unique(df):
    unique = {}
    uniques = []
    seen = []
    size = 2
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

def main():

    """
    This function will delete some IDs by replacing them by "DEL"
    """
    # create dataframe : REPLACE WITH THE RIGHT CSV
    column_names = ["ID", "DateTime", "X", "Y"]
    dtypes = {'ID': 'str', 'DateTime': 'str', 'X': 'float64', 'Y': 'float64'}
    parse_dates = ['DateTime']
    df = pd.read_csv('/Users/christinekhalil/Developer/SecuProject/Tests/Python/smallBDD.csv', sep='\t', header=None, names=column_names, dtype=dtypes, parse_dates=parse_dates)

    # find uniques after meet/tuile program
    not_del_array = unique(df) 
    
    #ajout de la colonne "index" dans la bdd en paramètres
    df['Index'] = range(0, len(df))

    # liste des ID uniques
    list_id = df['ID'].unique()

    # array des index des lignes dont on doit "DEL" l'id
    index_array = []

    # pour chaque ID unique 
    for id in list_id :
        # on crée un sous-tableau des lignes qui ont cet ID
        df_id = df[ df['ID'] == id ]
        # on transforme la date de ce sous-tableau 
        df_id['Week'] = df_id['DateTime'].dt.year.astype(str) + "-" + df_id['DateTime'].dt.week.astype(str)
        # puis on fait une liste des semaines uniques pour cet ID
        list_week = df_id['Week'].unique()
        # pour chaque semaine unique, on ajoute une partie des lignes dans la liste des lignes à supprimer index_array
        
        for week in list_week :
            df_week = df_id[ df_id['Week'] == week ] 
            size_array = len(df_week)
            random_tab = np.random.uniform(0,1,size_array)
            test_value = size_array/10000000
            if (test_value < 0.1) :
                test_value = 0.1
            random_bool = random_tab<test_value
            # création de la liste des index à True
            if (len(df_week.loc[random_bool,"Index"])<1):
                df_one_line = df.sample(n=1)
                index_array = [*index_array,*(df_one_line.loc[:,"Index"].tolist())]
            else : 
                index_array = [*index_array,*(df_week.loc[random_bool,"Index"].tolist())]
    # int to str type for all values in the ID column (to avoid problems with "DEL")
    df["ID"]=df["ID"].astype(str)

    # enlever les lignes importantes de la liste des lignes à supprimer
    for element in index_array:
        if element in not_del_array:
            index_array.remove(element)

    # int to str type for all values in the ID column (to avoid problems with "DEL")
    #df["ID"]=df["ID"].astype(str)
    # on "DEL" les id des lignes dans la liste index_id
    df.iloc[index_array, 0]="DEL"
    del df["Index"]
    print("Nombre de lignes supprimées : ",len(index_array))

    # randomisation des heures/min/sec sans faire attention aux POI pour l'instant
    df.iloc[index_array, 1]=df.iloc[index_array, 1].apply( lambda x : pd.datetime(x.year, x.month, x.day, random.randint(0,23),random.randint(0,59),random.randint(0,59) ))
    # randomisation des longitudes/latitudes : à fixer out of range pour ne pas impacter POI
    df.iloc[index_array, 2]=df.iloc[index_array, 2].apply( lambda x : 8000)
    df.iloc[index_array, 3]=df.iloc[index_array, 3].apply( lambda x : 8000)

    df.to_csv("result_naive.csv", index=False, header=False, sep='\t')


main()