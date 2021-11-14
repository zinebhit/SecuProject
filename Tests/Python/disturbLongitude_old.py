from math import *
from random import *

parameters = {'f1': [80,90,0,1], 'f2':[20000,40000,1000,3000], 'f3': [0.1, 0.14,0.08,0.081]}
j, k = 0, 0

def f1(x,param1,param2):
    return (exp(-param1)*(param1**x))/factorial(int(x))

def f2(x,param1,param2):
    return (1/(param1*sqrt(2*pi)))*exp(-0.5*(((x-param2)/param1)**2))

def f3(x,param1,param2):
    return exp(-(param1*x + ((param2*x)**2)*0.5))

#e.g: fun[0](9,3) is equivalent to f1(9,3)
functions = [f1,f2,f3]

#random works with reals and integers 

def f(x,limit,y):
    global j,k,currentID
    if currentID != y:
        currentID = y
        j = 0
    i = randint(0,2)
    x1, x2 = int(x*10000%10), int(x*100000%10)
    k = k + 1
    if((x1+x2)%3 == i and j < limit): 
        j = j + 1
        return x + randint(1,5)
    return x + functions[i](x,(randrange(parameters['f'+str(i+1)][0]*1000,parameters['f'+str(i+1)][1]*1000))/1000,(randrange(parameters['f'+str(i+1)][2]*1000,parameters['f'+str(i+1)][3]*1000))/1000)

def main(df, options):
    global currentID
    limit = 10000
    currentID = df['id'][0]
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : f(x,limit,df['id'][k]))
    return df