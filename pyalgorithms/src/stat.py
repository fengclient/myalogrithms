'''
Created on 2012-8-3

@author: fengclient
'''
import math
import random
import time
random.seed(time.ctime())

def stat(numbers):
    '''
    return statistic (arithmetic average, standard deviation) for numbers.
    '''
    if not (isinstance(numbers, list) or isinstance(numbers, tuple)):
        return (0, 0)
    if len(numbers) == 0:
        return (0, 0)
    aver = sum(numbers) / len(numbers)
    sum_diff = 0
    for i in numbers:
        sum_diff = sum_diff + (i - aver) ** 2
    return (aver, math.sqrt(sum_diff))

if __name__ == '__main__':
    #test stat
    numbers = [random.random() for x in range(10)]
    print 'numbers:', numbers
    print 'statistic:', stat(numbers)
