import random
import pandas as pd

# This is code in construction, it will be completed tomorrow ! 

#Change ids with random value for a whole interval that doesn't exceed the week limitation
# + group them to 

def main(df, options):
    # Max = result of total id numbers 
    # add condition of week here 

    # add condition of random change 
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : random.randint(0,Max))
    return df