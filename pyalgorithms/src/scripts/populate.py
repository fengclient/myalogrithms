#coding=utf-8
'''
Created on 2012-12-20

@author: fengclient

Dependency: web2py dal

'''
import sys
sys.path.append('/data/web2py')
from StringIO import StringIO
from time import time
import random
random.seed(time())
from gluon.dal import DAL,Field

def random_str_digital(length):
    builder= StringIO(length)
    for i in range(length):
        builder.write(random.choice('abcdefghijklmnopqrstuvwxyz1234567890'))
    ret=builder.getvalue()
    builder.close()
    return ret

def define_table(tablename,fieldcount):
    db = DAL('mysql://test:123456@localhost:3306/test')
    fields=[]
    fields.append(Field('id','id'))
    fields.extend([Field('field_%d'%i,'string') for i in range(fieldcount)])
    db.define_table(tablename,*fields)
    return db

def fuzz_fields(fields,stringlength=20):
    values=[None if i=='id' else random_str_digital(stringlength) for i in fields]
    return dict(zip(fields,values))      

def populate(rowcount,fieldcount=10):
    db=define_table('large',fieldcount)
    for i in range(rowcount):
        row=fuzz_fields(db.large.fields)
        db.large.insert(**row)
    db.commit()
        
if __name__ == '__main__':
    populate(10,10)
    