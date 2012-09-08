#coding=utf-8
'''
Created on 2012-5-7
i've changed to use jmeter as concurrent engine.
@author: fengclient
'''
from urllib2 import urlopen,HTTPError,URLError
from time import time
import random
random.seed(time())
from StringIO import StringIO
from threading import Timer
from multiprocessing import Process,Event,Queue
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

def run(msg_queue,stop_flag):
    req_counter=err_counter=time_cost=0
    while not stop_flag.is_set():
        #print 'thread(%d),count=%d'%(index,req_counter[index])
        start=time()
        try:
            #urlopen(r'http://s.com/convert?orig=http://%s/%d/%d'%(domain,index,req_counter[index]))
            #urlopen(r'http://s.com/40236')
            urlopen(r'http://www.baidu.com/')
        except HTTPError as e:
            err_counter=err_counter+1
        except URLError as e:
            err_counter=err_counter+1
        end=time()
        time_cost=time_cost+(end-start)
        req_counter=req_counter+1
    msg_queue.put((req_counter,err_counter,time_cost))

def throughput(seconds=10,cocurrency=1):
    '''
    seconds should be greater than or equal to 10
    1000w pv = 115 rps
    '''
    stop_flag=Event()
    processes=[]
    t=Timer(seconds,stop,args=[stop_flag])
    q = Queue()
    for i in range(cocurrency):
        processes.append(Process(target=run,args=(q,stop_flag)))
    t.start()
    for p in processes:
        p.start()
    #print 'start waiting for workers:',len(processes)
    stop_flag.wait()
    for t in processes:
        t.join()
    total=err=cost=0
    while not q.empty():
        (req_counter,err_counter,time_cost)=q.get()
        total=total+req_counter
        err=err+err_counter
        cost=cost+time_cost
    cost=cost/total if total>0 else 0

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
