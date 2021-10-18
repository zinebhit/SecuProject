from math import *
from random import *

parameters = {'f1': [80,90,0,1], 'f2':[20000,40000,1000,3000], 'f3': [0.1, 0.14,0.08,0.081]}
#lambda = 85 is the best: ordre de grandeur 10 ^ (-5)
#(exp(-lambdaa)*(lambdaa**x))/factorial(x)
def f1(x,param1,param2):
    return (exp(-param1)*(param1**x))/factorial(int(x))
    #return (exp(-85)*(85**x))/factorial(int(x))

#Best values for mu and sigma are 140 and 220 approx
#(1/(sigma*sqrt(2*pi)))*exp(-0.5*(((x-mu)/sigma)**2))
def f2(x,param1,param2):
    return (1/(param1*sqrt(2*pi)))*exp(-0.5*(((x-param2)/param1)**2))
    #return (1/(26000*sqrt(2*pi)))*exp(-0.5*(((x-1960)/26000)**2))

#Best values for mu and sigma are 0.05 and 0.08 or something similar
#exp(-(mu*x + ((sigma*x)**2)*0.5))
def f3(x,param1,param2):
    return exp(-(param1*x + ((param2*x)**2)*0.5))
    #return exp(-(0.05*x + ((0.08*x)**2)*0.5))

#e.g: fun[0](9,3) is equivalent to f1(9,3)
functions = [f1,f2,f3]

#random works with reals and integers 

def f(x):
    i = randint(0,2)
    return x + functions[i](x,(randrange(parameters['f'+str(i+1)][0]*1000,parameters['f'+str(i+1)][1]*1000))/1000,(randrange(parameters['f'+str(i+1)][2]*1000,parameters['f'+str(i+1)][3]*1000))/1000)

def main(df, options):
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : f(x))
    return df
