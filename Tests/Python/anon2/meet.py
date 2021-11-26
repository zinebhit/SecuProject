from random import randint
import pandas as pd
from math import sqrt
# pd.options.mode.chained_assignment = None


def main():
    unique = {}
    uniques = []
    seen = {}
    near = {}
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
    
    #Retrieve the unique positions for each id
    for i in range(len(df1.index)):
        if int(df1.iloc[i]['ID']) in unique.keys():
            unique[int(df1.iloc[i]['ID'])].append(tuple([df1.iloc[i]['X'],df1.iloc[i]['Y']]))
        else:
            uniques.append(int(df1.iloc[i]['ID']))
            unique[int(df1.iloc[i]['ID'])] = [tuple([df1.iloc[i]['X'],df1.iloc[i]['Y']])]
    uniques = list(set(uniques))
    
    x, y, x1, y1 = 0, 0, 0, 0
    for row in df_orig.iterrows():
        #row[0] --> index       row[1] --> content
        if int(row[1].ID) in unique.keys():
            if int(row[1].ID) not in seen.keys():
                seen[int(row[1].ID)] = []
            if tuple([round(row[1].X,size),round(row[1].Y,size)]) in unique[int(row[1].ID)]: continue
            else:
                if (round(row[1].X,size),round(row[1].Y,size)) not in seen[int(row[1].ID)]: 
                    seen[int(row[1].ID)].append(tuple([round(row[1].X,size),round(row[1].Y,size)]))
                else:
                    #l = randint(0,len(unique[int(row[1].ID)])-1)
                    # row[1].X, row[1].Y = unique[int(row[1].ID)][l]
                    #df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = unique[int(row[1].ID)][l]
                    tup = tuple([round(row[1].X,size), round(row[1].Y,size)])
                    if tup in near.keys():
                        df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = near[tup]
                    else:
                        near[tup] = nearest(unique[int(row[1].ID)], tuple([row[1].X, row[1].Y]))
                        df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = near[tup]
        else:
            if int(row[1].ID) not in seen.keys():
                seen[int(row[1].ID)] = []
            if (round(row[1].X,size),round(row[1].Y,size)) not in seen[int(row[1].ID)]: 
                seen[int(row[1].ID)].append(tuple([round(row[1].X,size),round(row[1].Y,size)])) 
            else:
                if (x == round(row[1].X,2) and y == round(row[1].Y,2)):
                    df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = x1, y1
                else:
                    k = randint(0,len(uniques)-1)
                    #l = randint(0,len(unique[uniques[k]])-1)
                    # df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = unique[uniques[k]][l]
                    # x1, y1 = unique[uniques[k]][l]
                    x, y = round(row[1].X,2), round(row[1].Y,2)
                    tup = tuple([round(row[1].X,size), round(row[1].Y,size)])
                    if tup in near.keys():
                        df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = near[tup]
                        x1, y1 = near[tup]
                    else:
                        near[tup] = nearest(unique[uniques[k]], tuple([row[1].X, row[1].Y]))
                        df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = near[tup]

    
    df_orig.to_csv("test_result1.csv", index=False, header=False, sep='\t')

    #TEST#
    # df = df.groupby(['ID']).size().reset_index(name='count')
    # df_orig['X'] = df_orig['X'].round(size)
    # df_orig['Y'] = df_orig['Y'].round(size)
    # df_orig = df_orig.groupby(['ID','X','Y']).size().reset_index(name='count')
    # df_orig = df_orig.groupby(['ID']).size().reset_index(name='count')
    # print(df)
    # print(df_orig)

def nearest(liste, tup):
    min = 100
    tuple_min = liste[0]
    for tup1 in liste: 
        distance = sqrt((tup1[0]-tup[0])**2 + (tup1[1]-tup[1])**2)
        if(distance < min):
            min = distance
            tuple_min = tup1
    return tuple_min

main()

#21 5 16 37 25