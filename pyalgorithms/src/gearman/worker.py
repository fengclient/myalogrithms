#coding=utf-8
'''
Created on 2012-5-20

@author: fengclient
'''
from BeautifulSoup import BeautifulSoup
from urllib2 import urlparse,HTTPError
from crawle_pic import *
from gearman.client import GearmanClient
from gearman.worker import GearmanWorker
from gearman import DataEncoder
from gearman.constants import *
import redis
import config
import sys
import logging
import logging.handlers
import json
import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyhttplib import myhttplib

class JSONDataEncoder(DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return json.dumps(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        return json.loads(decodable_string)

gm_client=GearmanClient([config.job_server])
gm_client.data_encoder=JSONDataEncoder

r_client = redis.StrictRedis(host=config.redis_server, port=config.redis_port, db=0)

def submit_html_job(url,delay=False):
    func_name = 'worker_process_html_delay' if delay else 'worker_process_html'
    job_req=gm_client.submit_job(func_name,url,
                                 background=True,wait_until_complete=False)
    return job_req.job.unique

def submit_pic_job(root_dir,title,url,delay=False):
    data=(root_dir,title,url)
    func_name = 'worker_process_pic_delay' if delay else 'worker_process_pic'
    job_req=gm_client.submit_job(func_name,data,
                                 background=True,wait_until_complete=False)
    return job_req.job.unique

def is_processed(url):
    return r_client.get(url.encode('utf8'))!=None

def set_processed(url,state=True):
    return r_client.set(url.encode('utf8'),state)

def worker_process_html(gearman_worker, gearman_job):
    url=gearman_job.data
    if is_processed(url):
        print url,'is skipped as it was processed already'
        return
    print 'processing',url
    try:
        html_doc=myhttplib.urlopen(url)[2]
    except HTTPError,e:
        print 'http error,',e.code
        set_processed(url,e.code)
        return
    except Exception,e:
        print e
        print url,' is delayed it to queue'
        submit_html_job(url,True)
        raise
    #this web is encoded by gbk
    html_doc=html_doc.decode('gbk')
    soup=BeautifulSoup(html_doc)
    if is_index(soup):
        pages=find_pages_from_index(soup,url)
        print '%d pages are found'%(len(pages))
        for p in pages:
            submit_html_job(p)
            print p,'is submitted'
        more_indexes=find_next_indexes(soup,url)
        print '%d sub indexes are found'%(len(more_indexes))
        for i in more_indexes:
            submit_html_job(i)
            print i,'is submitted'
    elif is_page(soup):
        title,pics=find_pics(soup,url)
        print '%d pictures are found'%(len(pics))
        for p in pics:
            submit_pic_job(config.root_dir,title,p)
            print p,'is submitted'
        more_pages=find_next_pages(soup,url)
        print '%d sub pages are found'%(len(more_pages))
        for p in more_pages:
            submit_html_job(p)
            print p,'is submitted'
    else:
        print 'unknown resource'
    set_processed(url)
            
def worker_process_pic(gearman_worker, gearman_job):
    root_dir,title,url=gearman_job.data
    if is_processed(url):
        print url,'is skipped as it was processed already'
        return
    print 'processing',url
    try:
        content=myhttplib.urlopen(url)[2]
    except HTTPError,e:
        print 'http error:',e.code
        set_processed(url,e.code)
        return
    except Exception,e:
        print e
        print url,' is delayed it to queue'
        submit_pic_job(root_dir,title,url,True)
        raise
    name=urlparse.urlparse(url).path.split('/')[-1]
    filepath=os.path.join(root_dir,title)
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    filepath=os.path.join(filepath,name)
    with open(filepath,'wb') as f:
        f.write(content)
    set_processed(url)
    print filepath,'is saved'
    
class SafeGearmanWorker(GearmanWorker):
    '''
    copied from http://packages.python.org/gearman/1to2.html#worker
    worker with exception logging and JSON encoder
    '''
    data_encoder=JSONDataEncoder
    logger=logging.getLogger('SafeGearmanWorker')
    logger.setLevel(logging.DEBUG)
    fh=logging.handlers.SocketHandler(config.logging_host,config.logging_port)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    def on_job_exception(self, current_job, exc_info):
        print "Job failed, CAN stop last gasp GEARMAN_COMMAND_WORK_FAIL"
        self.logger.error('exception: %s, %s'%(current_job,exc_info))
        self.logger.debug('%s,type:%s'%(self,super(SafeGearmanWorker, self))) 
        return super(SafeGearmanWorker, self).on_job_exception(current_job,exc_info)
    
    def after_poll(self,any_activity):
        self.logger.debug('after_pull,any_activity=%s'%(any_activity))
        print 'after_pull',any_activity
        return True

if __name__ == '__main__':
    worker=SafeGearmanWorker([config.job_server])
    worker.set_client_id('dummy_worker_client_id')
    if len(sys.argv)==2 and sys.argv[1]=='delay':
        worker.register_task('worker_process_html_delay', worker_process_html)
        worker.register_task('worker_process_pic_delay', worker_process_pic)
    else:
        worker.register_task('worker_process_html', worker_process_html)
        worker.register_task('worker_process_pic', worker_process_pic)
    worker.work()
