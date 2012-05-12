#coding=utf-8
'''
Created on 2012-5-7

@author: fengclient
'''
from urllib2 import urlopen
from time import time
import random
random.seed(time())
from StringIO import StringIO
from threading import Timer,Thread

#perf
#concurrency sched module
#thoughtput

def latecy():
    pass

def random_str_digital(length):
    builder= StringIO(length)
    for i in range(length):
        builder.write(random.choice('abcdefghijklmnopqrstuvwxyz1234567890'))
    ret=builder.getvalue()
    builder.close()
    return ret

domain=random_str_digital(20)

def response(count=100,cocurr=1):
    time_sum=0
    for i in xrange(count):
        start=time()
        urlopen(r'http://s.com/convert?orig=http://%s/%s'%(domain,i))
        end=time()
        time_sum+=(end-start)
    return time_sum/count

flag=True
counter=[]
threads=[]

def stop():
    global flag
    flag=False
    #print 'stop flag is set'

def run(counter,index):
    global flag,domain
    while flag:
        print 'thread(%d),count=%d'%(index,counter[index])
        urlopen(r'http://s.com/convert?orig=http://%s/%d/%d'%(domain,index,counter[index]))
        counter[index]=counter[index]+1
    #print 'thread(%d) is stopped'%(index)

def throughput(seconds=10,cocurrency=1):
    '''
    i got 808 in 60s with 1 user;
    1806 with 10 user
    1485 with 2 user
    '''
    global counter,threads
    t=Timer(seconds,stop)
    for i in range(cocurrency):
        counter.append(0)
        threads.append(Thread(target=run,args=(counter,i)))
    t.start()
    for thread in threads:
        thread.start()

def throughput_singlethread(seconds=10):
    '''
    i got 844 in 60s?
    '''
    global flag,domain
    t=Timer(seconds,stop)
    t.start()
    count=0
    while flag:
        print 'count=%d'%(count)
        urlopen(r'http://s.com/convert?orig=http://%s/%d'%(domain,count))
        count=count+1
    print 'stopped'
    return count

if __name__ == '__main__':
    #print 'response time:',response(10)
    print 'throughput time:',throughput(60,2),'per %d seconds'%(60)
    #print 'throughput time:',throughput_singlethread(60),'per %d seconds'%(60)
    