from math import *
from random import randint

j, k = 0,0

def f(x,limit,y):
    global j,k,currentID
    if currentID != y:
        currentID = y
        j = 0
    i = randint(0,2)
    x1, x2 = int(x*10000%10), int(x*100000%10)
    if((x1+x2)%3 == i and j < limit): 
        j = j + 1
        return x + randint(1,5)
    return x + randint(1,20)/10000

def main(df, options):
    global currentID
    limit = 10000
    currentID = df['id'][0]
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : f(x,limit,df['id'][k]))
    return df