#coding=utf-8
'''
Created on 2012-5-7

@author: fengclient
'''
from urllib2 import urlopen,HTTPError,URLError
from time import time
import random
random.seed(time())
from StringIO import StringIO
from threading import Timer,Thread,Event,Semaphore
from argparse import ArgumentParser

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
        time_sum=time_sum+(end-start)
    return time_sum/count

def stop(stop_flag):
    stop_flag.set()
    #print 'stop_flag is set'

def run(req_counter,err_counter,time_cost,index,stop_flag):
    while not stop_flag.is_set():
        #print 'thread(%d),count=%d'%(index,req_counter[index])
        start=time()
        try:
            #urlopen(r'http://s.com/convert?orig=http://%s/%d/%d'%(domain,index,req_counter[index]))
            urlopen(r'http://s.com/40236')
        except HTTPError as e:
            err_counter[index]=err_counter[index]+1
        except URLError as e:
            err_counter[index]=err_counter[index]+1
        end=time()
        time_cost[index]=time_cost[index]+(end-start)
        req_counter[index]=req_counter[index]+1
    #print 'thread(%d) is stopped'%(index)

def throughput(seconds=10,cocurrency=1):
    '''
    seconds should be greater than or equal to 10
    1000w pv = 115 rps
    '''
    stop_flag=Event()
    req_counter=[]
    err_counter=[]
    time_cost=[]
    threads=[]
    t=Timer(seconds,stop,args=[stop_flag])
    for i in range(cocurrency):
        req_counter.append(0)
        err_counter.append(0)
        time_cost.append(0)
        threads.append(Thread(target=run,args=(req_counter,err_counter,time_cost,i,stop_flag)))
    t.start()
    for thread in threads:
        thread.start()
    #print 'start waiting for workers:',len(threads)
    stop_flag.wait()
    for t in threads:
        t.join()
    total=sum(req_counter)
    err=sum(err_counter)
    cost=sum(time_cost)/total if total>0 else 0
    return total,err,cost

def reset():
    return urlopen(r'http://s.com/reset')

def extract_exec_time_from_access_log(path):
    '''
    used to extract average execution time from microtime data in apache access file
    '''
    detail=[]
    with open(path) as f:
        line=f.readline()
        while line:
            cost = float(line.split(' ')[0]) / 10000
            detail.append(cost)
            line=f.readline()
    return detail

def populate(count=100000):
    '''
    populate records
    '''
    import sys
    sys.path.append(r'D:\Workbench\private\web2py_src\applications\welcome\models')
    db=__import__('db')
    i=0
    while i<count:
        db.db.orig_to_short.insert(originalurl=r'http://%s/%d'%(domain,i),shorturl=repr(i))
        if i%10000==0:
            db.db.commit()
            print '%d is reached'%(i)
        i=i+1
    db.db.commit()
    print '%d is finished'%(i)

def take_benchmark():
    test_pairs=[(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10,10)]
    print '--------------------------thoughtput test on s.com---------------------------'
    print 'time\tusers\trequests\terrors\taver_resp_time\tfail-rate'
    for seconds,users in test_pairs:
        ret=throughput(seconds,users)
        print '%d\t%d\t%d\t%d\t%f\t%f'%(seconds,users,ret[0],ret[1],ret[2],float(ret[1])/ret[0] if ret[0]>0 else 0)

if __name__ == '__main__':
    parser = ArgumentParser(description = 'benchmark')
    parser.add_argument('-b','--benchmark', action='store_true',help= 'take benchmark')
    parser.add_argument('-po','--populate', type=int,metavar='<count>',help= 'populate databases')
    parser.add_argument('-p','--parselog', metavar='<file>',help='extract average execution time from microtime data in apache access log file')
    ns = parser.parse_args()
    if ns.benchmark:
        take_benchmark()
    elif ns.populate:
        populate(ns.populate)
    elif ns.parselog:
        details=extract_exec_time_from_access_log(ns.parselog)
        print 'count=%d,average=%f'%(len(details),sum(details)/len(details))
    else:
        print 'args error?'
