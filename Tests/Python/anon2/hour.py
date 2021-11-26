from datetime import *
from random import randint

def hourModify(date):
    print(date.isoweekday())
    hours = [6, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22] if(0 <= date.weekday() <= 4) else [18, 19, 20, 21, 22, 23, 0, 1, 2 , 3, 4, 5, 6, 7, 8, 9, 10] 
    limits = [6 , 9, 16, 22] if(1 <= date.isoweekday() <= 5) else [10,18]
    h , m , s = hours[randint(0,len(hours)-1)], 0 , 0
    if h not in limits:
        m, s = randint(0,59), randint(0,59)
    return datetime(date.year,date.month,date.day,h,m,s)


# [Monday,Tuesday,..., Sunday] => [0,1,...6]
# date = datetime(2021,11,26)
# print(hourModify(date))