import pandas as pd
import random

def sacrifice(x, a, b, c):
    # for lines concerned by POI
    if (x.hour<6 or x.hour>22 or (x.hour>9 and x.hour<16) ):
        sacrifice_number = random.randint(1, b)
        if (sacrifice_number == b) :
            # keep "it's night time" information
            if (x.hour<6 or x.hour>22) :
                second_sacrifice = random.randint(1, c)
                if (second_sacrifice == c) :
                    return (pd.datetime(x.year, x.month, x.day, random.randint(0, 23) , random.randint(0, 59) , random.randint(0, 59)))    
                else : 
                    return (pd.datetime(x.year, x.month, x.day, random.choice([23,0,1,2,3,4,5]) ,random.randint(0, 59) , random.randint(0, 59)))
            # keep "it's work time" information
            elif ((x.hour)>9 and (x.hour)<16) :
                second_sacrifice = random.randint(1, c)
                if (second_sacrifice == c) :
                    return (pd.datetime(x.year, x.month, x.day, random.randint(0, 23) , random.randint(0, 59) , random.randint(0, 59)))    
                else : 
                    return (pd.datetime(x.year, x.month, x.day, random.randint(10, 15) ,random.randint(0, 59) , random.randint(0, 59)))
        else :
            return (pd.datetime(x.year, x.month, x.day, x.hour , x.minute , x.second )) 
    # we don't care about other hours because they're not concerned by POI so we random them completely
    else :
        # hours not concerned by POI : high probability to be destroyed 
        sacrifice_number = random.randint(1, a)
        if (sacrifice_number == a) :
            return (pd.datetime(x.year, x.month, x.day, random.randint(0, 23) , random.randint(0, 59) , random.randint(0, 59)))    
        else :
          # when sacrifice_number != a : the line is not sacrificed ! return the same line
            return (pd.datetime(x.year, x.month, x.day, x.hour , x.minute , x.second )) 



def hour_sacrifice(df, options):
        df.loc[:,column] = df.loc[:,column].apply(sacrifice, args=params)
        return df