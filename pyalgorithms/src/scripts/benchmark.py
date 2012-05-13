#coding=utf-8
'''
Created on 2012-5-7

@author: fengclient
'''
from urllib2 import urlopen,HTTPError
from time import time
import random
random.seed(time())
from StringIO import StringIO
from threading import Timer,Thread,Event,Semaphore

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

def stop(stop_flag):
    stop_flag.set()
    #print 'stop_flag is set'

def run(req_counter,err_counter,index,stop_flag,pool_threads):
    pool_threads.acquire()
    while not stop_flag.is_set():
        #print 'thread(%d),count=%d'%(index,req_counter[index])
        try:
            urlopen(r'http://s.com/convert?orig=http://%s/%d/%d'%(domain,index,req_counter[index]))
        except HTTPError as e:
            #print 'http exception is catched:',e
            err_counter[index]=err_counter[index]+1
        req_counter[index]=req_counter[index]+1
    #print 'thread(%d) is stopped'%(index)
    pool_threads.release()

def throughput(seconds=10,cocurrency=1):
    '''
    i got 808 in 60s with 1 user;
    1806 with 10 user
    1485 with 2 user
    '''
    stop_flag=Event()
    pool_threads=Semaphore(cocurrency)
    req_counter=[]
    err_counter=[]
    threads=[]
    t=Timer(seconds,stop,args=[stop_flag])
    for i in range(cocurrency):
        req_counter.append(0)
        err_counter.append(0)
        threads.append(Thread(target=run,args=(req_counter,err_counter,i,stop_flag,pool_threads)))
    t.start()
    for thread in threads:
        thread.start()
    #print 'start waiting for workers'
    i=0
    while i<cocurrency and pool_threads.acquire():
        #print 'one worker is finished'
        i=i+1
    return sum(req_counter),sum(err_counter)

def throughput_singlethread(seconds=10):
    '''
    i got 844 in 60s?
    '''
    stop_event=Event()
    t=Timer(seconds,stop_event)
    t.start()
    count=0
    while not stop_event.is_set():
        #print 'count=%d'%(count)
        urlopen(r'http://s.com/convert?orig=http://%s/%d'%(domain,count))
        count=count+1
    #print 'execution is stopped'
    return count

def reset():
    return urlopen(r'http://s.com/reset')

if __name__ == '__main__':
    #print 'response time:',response(10)
    test_pairs=[(10,1),(10,2),(10,3),(10,4),(10,5),
                (10,6),(10,7),(10,8),(10,9),(10,10)]
    for seconds,users in test_pairs:
        reset()
        ret=throughput(seconds,users)
        print 'throughput in %ds with %d users: %d requests with %d errors, fail rate=%f'\
                %(seconds,users,ret[0],ret[1],float(ret[1])/ret[0])

#    ret=throughput(600,3)
#    print 'throughput in %ds with %d users: %d requests with %d errors, fail rate=%f'\
#                %(600,3,ret[0],ret[1],float(ret[1])/ret[0])
    