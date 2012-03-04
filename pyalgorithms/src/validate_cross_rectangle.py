'''
Created on 2012-3-2
Implement the following C# function to determine if 2 rectangles 
overlap or touch each other. The rectangles run parallel to the x and y axes.

@author: fengclient
'''
import sys
from argparse import ArgumentParser

if __name__ == '__main__':
    print 'your argv:', sys.argv
    parser = ArgumentParser(description = 'validate if rectangle has overlap')
    parser.add_argument('rect', nargs = 2, metavar = '(x,y,width,length)')
    ns = parser.parse_args()
    b = eval(ns.rect[0])
    c = eval(ns.rect[1])
    print 'rect:', b, c
    #relocate them
    b1 = (b[0], b[0] + b[2], b[1], b[1] + b[3])
    c1 = (c[0], c[0] + c[2], c[1], c[1] + c[3])
    if (b[1] > c[0] or b[0] < c[1]) and (b[2] < c[3] or b[3] > c[2]):
        print 'yes, they have overlap'
    else:
        print "no, they don't have overlap"
