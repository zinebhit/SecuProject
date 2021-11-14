from math import *
from random import *

parameters = {'f1': [15,18,0,1], 'f2':[40,80,10,100], 'f3': [0.3, 0.8,0.3,0.8]}
j = 1

#lambda = 12 is the best
#(exp(-lambdaa)*(lambdaa**x))/factorial(x)
def f1(x,param1,param2):
    return (exp(-12)*(12**x))/factorial(int(abs(x)))

#Best values for mu and sigma are 45 and 10 approx
#(1/(sigma*sqrt(2*pi)))*exp(-0.5*(((x-mu)/sigma)**2))
def f2(x,param1,param2):
    return (1/(param1*sqrt(2*pi)))*exp(-0.5*(((x-param2)/param1)**2))
    #return (1/(45*sqrt(2*pi)))*exp(-0.5*(((x-10)/45)**2))

#Best values for mu and sigma are 0.0009 and 0.8 or something similar
#exp(-(mu*x + ((sigma*x)**2)*0.5))
def f3(x,param1,param2):
    return exp(-(param1*x + ((param2*x)**2)*0.5))
    #return exp(-(0.0009*x + ((0.8*x)**2)*0.5))

#e.g: fun[0](9,3) is equivalent to f1(9,3)
functions = [f1,f2,f3]

def f(x,limit):
    global j
    i, k = randint(0,2), randint(0,10)
    x1, x2 = int(x*10000%10), int(x*100000%10)
    # if((x1+x2)%3 == i and j < limit): 
    if((x1+x2)%3 == i and j < limit): 
        j = j + 1
        return ((-1)**i)*(x - randint(1,5))
    # return ((-1)**(i+k))*(x + ((-1)**k)*randint(1,20)/10000)
    if i == 2: 
        p1, p2 = randrange(parameters['f3'][0]*10, parameters['f3'][1]*10)/10, randrange(parameters['f3'][2]*10, parameters['f3'][3]*10)/10
    else: p1,p2 = randrange(parameters['f'+str(i+1)][0],parameters['f'+str(i+1)][1]), randrange(parameters['f'+str(i+1)][2],parameters['f'+str(i+1)][3])
    
    return ((-1)**i)*(x + ((-1)**k)*functions[i](x,p1,p2))

def main(df, options):
    #print(options['column'])
    # df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : x + functions[int(round(x,4)*1000%10)%3-1](x))
    # #df['latitude'] = df['latitude'].shift()

    #The limit will depend on the number of lines we have in the dataframe, this line of code should be placed in the key file 
    limit = 10000
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : f(x,limit))
    return df
