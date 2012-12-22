#coding=utf-8
'''
Created on 2012-12-21

@author: fengclient
'''
import sys
from ctypes import *

def internal_case_hash(c):
    c=ord(c)
    return c & ~ ( ( c & 0x40 ) >> 1)

def internal_string_hash(s):
    print 'internal_string_hash to',s
    hashv=0x123
    for c in s:
        print 'get',c,ord(c)
        h=internal_case_hash(c)
        print 'value',h
        hashv=c_ulonglong(c_ulonglong(hashv*101).value+h).value
        print 'after hash',hashv
    return hashv

def StringHash(s,left,right):
    length=len(s)
    if not s or not length:
        return 0
    start=length+left if left<0 else left-1
    end=length+right if right<0 else right-1
    
    if start<0:
        start=0
    if end>=length:
        end=length-1
    return internal_string_hash(s[start:end+1])

if __name__ == '__main__':
    if len(sys.argv)<2:
        print 'stringhash.py <string>'
    else:
        s=sys.argv[1]
        print s
        print StringHash(s,1,-1)
