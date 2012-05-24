#coding=utf-8
'''
Created on 2012-5-20

@author: fengclient
'''

from gearman.client import GearmanClient
from gearman.worker import GearmanWorker
from gearman.constants import *
from pprint import pprint

def check_request_status(job_request):
    if job_request.complete:
        print "Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result)
    elif job_request.timed_out:
        print "Job %s timed out!" % job_request.unique
    elif job_request.state == JOB_UNKNOWN:
        print "Job %s connection failed!" % job_request.unique

if __name__ == '__main__':
    gm_client=GearmanClient(['localhost:4730'])
    job_req=gm_client.submit_job('reversed', 'fuzzing data')
    print 'job request:'
    pprint(dir(job_req))
    check_request_status(job_req)
