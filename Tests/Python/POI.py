from numpy.lib.arraysetops import unique
import pandas as pd
import numpy as np
from random import *


def function(df,indices):
    Weeks = df["week"].unique()
    output={}
    for week in Weeks:
        output[week]=[]
    for i in indices:
        output[df.at[i,"week"]].append(i)
    return output







def main():
    size = 2
    column_names = ["ID", "DateTime", "X", "Y"]
    column_names_comp = ["ID","section", "X", "Y","POICount"]

    dtypes = {'ID': 'str', 'DateTime': 'str', 'X': 'float64', 'Y': 'float64'}
    parse_dates = ['DateTime']

    column_namesComp = ["ID","section","X","Y","POICount"]
    dtypesComp = {'ID': 'str',"section":'str','X': 'float64', 'Y': 'float64','POICount': 'float64'}

    

    df = pd.read_csv('/Users/zinebhitait/Developer/SecuProject/Tests/Python/my_truth.csv', sep='\t', header=None, names=column_names, dtype=dtypes, parse_dates=parse_dates)
    df_orig = df.copy()

    dfComp= pd.read_csv('/Users/zinebhitait/Developer/SecuProject/Tests/Python/poidatacomp.csv', sep='\t',header=None,names=column_names_comp,dtype=dtypesComp)
    df_orig_comp = dfComp.copy()
    #dictionaire 

    POIunique = {}
    ModifIndex={}
    

    df['X'] = df['X'].round(size)
    df['Y'] = df['Y'].round(size)
    df["week"]=df['DateTime'].dt.isocalendar().week 

# retreive index lines concernées par la POI
    for row in df_orig_comp.iterrows():
        if row[1].ID not in POIunique.keys():
            POIunique[row[1].ID]= [[row[1].X,row[1].Y]]
        else:
            POIunique[row[1].ID].append([row[1].X,row[1].Y])

    for i in POIunique.keys():
        ModifIndex[i] = []

    for row in df.iterrows():
        if ([row[1].X, row[1].Y] in POIunique[row[1].ID]):
            ModifIndex[row[1].ID].append(row[0])
    print(ModifIndex)

  
            
    
    # l=function(df1.loc[df1['ID']=='1'],ModifIndex[1])
    # return(l)
    







    

print(main())





    # for i in ids : 
    #     while df['ID']== i :
    #         unique[1].append(tuple([dfComp.iloc[1]['X'],dfComp.iloc[1]['Y']]))
    #     i+1

        #     unique[int(df.iloc[i]['ID'])]
        # if int(df1.iloc[i]['ID']) in unique.keys():
        #     unique[int(df1.iloc[i]['ID'])].append(tuple([df1.iloc[i]['X'],df1.iloc[i]['Y']]))
        # else:
        #     uniques.append(int(df1.iloc[i]['ID']))
        #     unique[int(df1.iloc[i]['ID'])] = [tuple([df1.iloc[i]['X'],df1.iloc[i]['Y']])]

    #df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : )
    
    #df['LLMatch'] = np.where(((df['X'] == dfComp['X'])&(df['Y']== dfComp['Y'])),0,1) #create a new column in df1 for price diff
    
    #df.to_csv("test_poi.csv", index=False, header=False, sep='\t')

    #Changing minutes and seconds to have random values 
    #randValue1=randint(0,59)
    #randValue2=randint(0,59)
    #df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : pd.datetime(x.year, x.month, x.day, x.hour,random.randint(0,randValue1),random.randint(0,randValue2)))
    
    #I count number of lines for first POI 

#dans df je crée une sous df en selectionnant du ground truth les x et y dans les fichier de Data
#variable durée qui elle s'incrémente ou décrémente aléatoirement et modifie  


