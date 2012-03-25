#coding=utf-8
'''
Created on 2012-3-24

@author: fengclient
'''
from http_parser.pyparser import HttpParser

if __name__ == '__main__':
    rsp = open('d:\\172_request.txt').read()
    rsp = rsp.replace('\n', '\r\n')
    print rsp.find("\n")
    print rsp.find("\r\n")
    p = HttpParser()
    p.execute(rsp, len(rsp))
    print p.get_headers()
