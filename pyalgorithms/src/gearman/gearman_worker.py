#coding=utf-8
'''
Created on 2012-5-20

@author: fengclient
'''

from gearman.client import GearmanClient
from gearman.worker import GearmanWorker
from gearman.constants import *
from pprint import pprint

def reverse_data(worker,job):
    print 'worker:',worker.worker_client_id
    print 'job:',job.unique,job.connection,job.data,job.task
    return job.data[::-1]
    
if __name__ == '__main__':
    worker=GearmanWorker(['localhost:4730'])
    worker.set_client_id('dummy_worker_client_id')
    worker.register_task('reversed', reverse_data)
    worker.work()
    
