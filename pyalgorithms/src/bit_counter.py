#coding=utf-8
'''
Created on 2012-3-4
对一个二进制数中的0计数

@author: fengclient
'''

def count_1_by_iterate(byte):
    count = 0
    shift = 0x1
    for i in range(8):
        shift = 0x1 << i
        if byte & shift == shift:
            count = count + 1
    return count

def count_1_by_recursion(byte):
    if byte == 0:
        return 0
    a = 1 if byte & 0x1 == 0x1 else 0
    return a + count_1_by_recursion(byte >> 1)

if __name__ == '__main__':
    byte = 97
    count_1 = count_1_by_iterate(byte)
    count_2 = count_1_by_recursion(byte)
    
    print 'there are %s \'1\' in binary %s' % (count_1, bin(byte))
    print 'there are %s \'1\' in binary %s' % (count_2, bin(byte))
