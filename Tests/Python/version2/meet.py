from random import randint
import pandas as pd
# pd.options.mode.chained_assignment = None


def main():
    unique = {}
    uniques = []
    seen = []
    size = 2
    column_names = ["ID", "DateTime", "X", "Y"]
    dtypes = {'ID': 'str', 'DateTime': 'str', 'X': 'float64', 'Y': 'float64'}
    parse_dates = ['DateTime']
    df = pd.read_csv('/Users/christinekhalil/Downloads/groundTruth.csv', sep='\t', header=None, names=column_names, dtype=dtypes, parse_dates=parse_dates)
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

    # for row in df1.itertuples():
    #     #row[0] --> index   row[1] --> ID   row[2] --> X    row[3] --> Y
    #     if int(row[1]) in unique.keys():
    #         unique[int(row[1])].append(tuple([row[2],row[3]]))
    #     else:
    #         uniques.append(int(row[1]))
    #         unique[int(row[1])] = [tuple([row[2],row[3]])]

    #df2 = df.loc[(df['count'] != 1) & (df['ID'] == 1)]
    #I can do it in a very random way
    x, y, x1, y1 = 0, 0, 0, 0
    #id, x, y = 0, 0, 0
    for row in df_orig.iterrows():
        #row[0] --> index       row[1] --> content
        if int(row[1].ID) in unique.keys():
            if tuple([row[1].X,row[1].Y]) in unique[int(row[1].ID)]: continue
            else:
                if (round(row[1].X,size),round(row[1].Y,size)) not in seen: 
                    seen.append(tuple([round(row[1].X,size),round(row[1].Y,size)]))
                else:
                    l = randint(0,len(unique[int(row[1].ID)])-1)
                    # row[1].X, row[1].Y = unique[int(row[1].ID)][l]
                    df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = unique[int(row[1].ID)][l]
        else: 
            if (x == round(row[1].X,2) and y == round(row[1].Y,2)):
                df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = x1, y1
            else:
                k = randint(0,len(uniques)-1)
                l = randint(0,len(unique[uniques[k]])-1)
                df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = unique[uniques[k]][l]
                x1, y1 = unique[uniques[k]][l]
                x, y = round(row[1].X,2), round(row[1].Y,2)
            # if id == int(row[1].ID):
            #     df_orig.at[row[0],'X'],df_orig.at[row[0],'Y'] = x, y
            # else:
            #     k = randint(0,len(uniques)-1)
            #     l = randint(0,len(unique[uniques[k]])-1)
            #     x, y = unique[uniques[k]][l]
            #     id = int(row[1].ID)

    # df_orig.at[0,'X'] = 1
    
    #print(df_orig)
    df_orig.to_csv("test_result.csv", index=False, header=False, sep='\t')

    #Mettre une colonne ou j'indique quelles sont les valeurs importantes celle ou l'occurence == 1
    #TEST#
    # df = df.groupby(['ID']).size().reset_index(name='count')
    # df_orig = df_orig.groupby(['ID','X','Y']).size().reset_index(name='count')
    # df_orig = df_orig.groupby(['ID']).size().reset_index(name='count')
    #print(df)
    #print(df_orig)

main()

#21 5 16 37 25