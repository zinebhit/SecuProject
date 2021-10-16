from math import *

int(round(7.5141111,4)*1000%10)

#lambda = 60 is the best
#(exp(-lambdaa)*(lambdaa**x))/factorial(x)
def f1(x):
    return (exp(-80)*(80**x))/factorial(int(x))

#Best values for mu and sigma are 140 and 220 approx
#(1/(sigma*sqrt(2*pi)))*exp(-0.5*(((x-mu)/sigma)**2))
def f2(x):
    return (1/(220*sqrt(2*pi)))*exp(-0.5*(((x-140)/220)**2))

#Best values for mu and sigma are 0.05 and 0.08 or something similar
#exp(-(mu*x + ((sigma*x)**2)*0.5))
def f3(x):
    return exp(-(0.05*x + ((0.08*x)**2)*0.5))

#e.g: fun[0](9,3) is equivalent to f1(9,3)
functions = [f1,f2,f3]

def main(df, options):
    #print(options['column'])
    df.loc[:,options['column']] = df.loc[:,options['column']].apply( lambda x : x + functions[int(round(x,4)*1000%10)%3-1](x))
    return df
