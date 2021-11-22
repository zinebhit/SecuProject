import numpy as np

def main (df, options):
    
    size_array = len(df)
    random_tab = np.random.uniform(0,1,size_array)
    df[options['column']]=df[options['column']].astype(str)

    random_bool = random_tab<0.3
    #returns [False,False,True,...] array
    df.loc[random_bool,options['column']] = "DEL"
    #delete 30% of IDs