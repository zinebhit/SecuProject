from math import *
from random import randint

j = 0

#lambda = 12 is the best
#(exp(-lambdaa)*(lambdaa**x))/factorial(x)
def f1(x):
    return (exp(-12)*(12**x))/factorial(int(abs(x)))

#Best values for mu and sigma are 45 and 10 approx
#(1/(sigma*sqrt(2*pi)))*exp(-0.5*(((x-mu)/sigma)**2))
def f2(x):
    return (1/(45*sqrt(2*pi)))*exp(-0.5*(((x-10)/45)**2))

#Best values for mu and sigma are 0.0009 and 0.8 or something similar
#exp(-(mu*x + ((sigma*x)**2)*0.5))
def f3(x):
    return exp(-(0.0009*x + ((0.8*x)**2)*0.5))

#e.g: fun[0](9,3) is equivalent to f1(9,3)
functions = [f1,f2,f3]

def f(x,limit):
    global j
    i = randint(0,2)
    x1, x2 = int(x*10000%10), int(x*100000%10)
    if((x1+x2)%3 == i and j < limit): 
        j = j + 1
        return x + randint(1,5)
    return x + randint(1,20)/10000

def main(df, options):
    #print(options['column'])
    # df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : x + functions[int(round(x,4)*1000%10)%3-1](x))
    # #df['latitude'] = df['latitude'].shift()

    #The limit will depend on the number of lines we have in the dataframe, this line of code should be placed in the key file 
    limit = df.index.stop/100
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : f(x,limit))
    return df
