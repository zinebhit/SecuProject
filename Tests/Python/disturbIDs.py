import random
import pandas as pd


#Change ids with random value for a whole interval that doesn't exceed the week limitation

# def f(x):
#     if x in IDS :
#         x=1
#         for week in Weeks :
#                 newId=random.randint(0,69)
#                 df.loc[(df['week']==week) &(df['id']==i) ,'id']= newId
#     else:
#         return x
#     pass

def main(df, options):
    #number of IDS
    #print(df.loc[:,options['column']].value_counts().to_csv())
    column = options["column"]
    df["week"]=df['date'].dt.isocalendar().week 
    #to see number of weeks 
    #print(df["week"].value_counts().to_csv()) 
    print(df['id'].unique())
    ids=df['id'].unique()
    #IDS = pd.array([4,50,69,42,62,72,59,6,2,67,7, 73, 27, 8, 1, 51, 75, 31, 13, 87, 53, 24, 28, 17, 81, 26, 9, 38, 41, 43, 83, 30, 52, 55, 60, 49, 65, 36, 44, 11, 32, 66, 68, 15, 14, 18, 39, 63, 71, 89, 78, 54, 35, 23, 37, 34, 16, 58, 21,77, 25, 107, 70, 29, 110, 48, 84, 5, 98])
    Weeks =df["week"].unique()
    #pd.array([11,13,10,12,15,14,16,19,17,18,20])
    
    #restIDS=[]
    for i in ids :
         # add condition of week + IDs: we alter ids in a limit of a week randomly at first
         for week in Weeks :
    #         # newId=random.randint(0,69)
    #         # if (df['week']==week) &(df['id']==i) :
    #         #     df['id']=newId
    #         # else :
    #         #     pass
            df.loc[(df['week']==week) &(df['id']==i),'id']= random.choice(ids)
    #df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : random.choice(ids))

    del df["week"]
    return df


