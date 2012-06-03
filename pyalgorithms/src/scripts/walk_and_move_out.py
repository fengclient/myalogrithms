#coding=utf-8
'''
orginaize the dir tree with prefix_index.ext

Created on 2012-5-31

@author: fengclient
'''

import os
import sys
   
def work_and_move_out(path):
    for dirname, dirnames, filenames in os.walk(path):
        print 'enter:',dirname
        if dirname!='.':
            for i in range(len(filenames)):
                old=os.path.join(path,dirname,filenames[i])
                dst=os.path.join(path,'%s_%d%s'%(dirname,i,os.path.splitext(filenames[i])[1]))
                os.rename(old, dst)

if __name__ == '__main__':
    if len(sys.argv)==2:
        work_and_move_out(sys.argv[1])
    else:
        print 'usage: work_and_move_out.py dirpath'
