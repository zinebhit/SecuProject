from math import *
from random import *

parameters = {'f1': [70,90,0,1], 'f2':[70,700,100,500], 'f3': [0.1, 0.14,0.08,0.081]}
j = 1

#(exp(-lambdaa)*(lambdaa**x))/factorial(x)
def f1(x,param1,param2):
    return (exp(-param1)*(param1**x))/factorial(int(x))
    #return (exp(-85)*(85**x))/factorial(int(x))


#(1/(sigma*sqrt(2*pi)))*exp(-0.5*(((x-mu)/sigma)**2))
def f2(x,param1,param2):
    return (1/(param1*sqrt(2*pi)))*exp(-0.5*(((x-param2)/param1)**2))
    #return (1/(26000*sqrt(2*pi)))*exp(-0.5*(((x-1960)/26000)**2))


#exp(-(mu*x + ((sigma*x)**2)*0.5))
def f3(x,param1,param2):
    return exp(-(param1*x + ((param2*x)**2)*0.5))
    #return exp(-(0.05*x + ((0.08*x)**2)*0.5))

#e.g: fun[0](9,3) is equivalent to f1(9,3)
functions = [f1,f2,f3]

#random works with reals and integers 

def f(x,limit):
    global j, currentIDI
    i, k = randint(0,2), randint(0,10)
    x1, x2 = int(x*10000%10), int(x*100000%10)
    if((x1+x2)%3 == i and j < limit): 
        j = j + 1
        return x + randint(1,10) + ((-1)**k)*randint(1,9)/10 + ((-1)**k)*randint(1,9)/100
    return x + ((-1)**k)*functions[i](x,(randrange(parameters['f'+str(i+1)][0]*1000,parameters['f'+str(i+1)][1]*1000))/1000,(randrange(parameters['f'+str(i+1)][2]*1000,parameters['f'+str(i+1)][3]*1000))/1000)

def main(df, options):
    #limit = df.index.stop/100
    limit = 10000
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : f(x,limit))
    return df
