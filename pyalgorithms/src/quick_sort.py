'''
Created on 2012-8-3

@author: fengclient
'''
import math
import random
import time
random.seed(time.ctime())

def quick_sort(numbers):
    q_sort(numbers, 0, len(numbers) - 1)
    
def q_sort(numbers, left, right):
    '''
    sort numbers by quick sort. complexity: O(n*logn)
    '''
    #print 'partition from %d to %d' % (left, right)
    #print 'before partition:', numbers
    if left >= right:
        return
    l = left
    r = right
    base_value = numbers[left]
    while(l < r):
        while(l <= r and numbers[l] <= base_value):
            l = l + 1
        while(r >= l and numbers[r] > base_value):
            r = r - 1
        if l < r:
            #swap
            tmp = numbers[l]
            numbers[l] = numbers[r]
            numbers[r] = tmp
    middle = r
    #print ' after partition:', numbers
    #print 'middle:', middle
    #swap
    #raw_input()
    tmp = numbers[left]
    numbers[left] = numbers[middle]
    numbers[middle] = tmp
    q_sort(numbers, left, middle - 1)
    q_sort(numbers, middle + 1, right)

if __name__ == '__main__':
    numbers = [random.randint(0, 100) for x in range(10)]
    print 'numbers:', numbers
    quick_sort(numbers)
    print 'final:', numbers
