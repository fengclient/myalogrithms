#coding=utf-8
'''
Created on 2012-5-20

@author: fengclient
'''

from gearman.client import GearmanClient
from gearman.worker import GearmanWorker
from gearman.job import GearmanJob
from gearman.constants import *
import crawle_pic
from worker import JSONDataEncoder
import redis
import config

def check_request_status(job_request):
    if job_request.complete:
        print "Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result)
    elif job_request.timed_out:
        print "Job %s timed out!" % job_request.job.unique
    elif job_request.state == JOB_UNKNOWN:
        print "Job %s connection failed!" % job_request.job.unique

if __name__ == '__main__':
    gm_client=GearmanClient([config.job_server])
    gm_client.data_encoder=JSONDataEncoder
    #url='http://www.ttkzm.com/html/pic/'
    url='http://www.ttkzm.com/html/pic/2012/7/10211069.html'
    #url='http://www.ttkzm.com/html/VIP/1/'
    print 'clear cache before submit'
    r_client = redis.StrictRedis(host=config.redis_server, port=config.redis_port, db=0)
    r_client.delete(url)
    print 'submitting index',url
    gm_client.submit_job('worker_process_html',url)
    
