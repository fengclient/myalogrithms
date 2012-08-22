'''
Created on 2012-2-25

@author: fengclient

simple wrapper for urllib2 with cookie support(by cookielib)
'''
import cookielib
import gzip, zlib, struct
from StringIO import StringIO
from urllib2 import HTTPCookieProcessor, HTTPRedirectHandler,\
                    HTTPDefaultErrorHandler, build_opener, Request, socket
from http_parser.pyparser import HttpParser

socket.setdefaulttimeout(10)

class MyHTTPRedirectHandler(HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return fp

    http_error_301 = http_error_303 = http_error_307 = http_error_302
     
def urlopen(url, data = None, cookiejar = None):
    '''
    get url content and store cookies. rfc2964 default cookie policy with domain strict is applied.
    (http_message,cookiejar,resp_data) is returned. resp_data is decoded if gzip/deflate is present.
    '''
    policy = cookielib.DefaultCookiePolicy(rfc2965 = True, strict_ns_domain = cookielib.DefaultCookiePolicy.DomainStrict)
    cj = cookielib.CookieJar(policy)
    cookiehandler = HTTPCookieProcessor(cj)
    redirect_handler = MyHTTPRedirectHandler()
    opener = build_opener(cookiehandler,redirect_handler)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
        'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
        'Accept-Language': 'en-gb,en;q=0.5',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Connection': 'keep-alive',
        'Accept-encoding': 'gzip,deflate'
    }
    req = Request(url, headers = headers)
    req.add_data(data)
    resp = opener.open(req)
    resp_data = resp.read() if resp!=None else None
    if resp and resp_data:
        # copied from feedparser.py(http://code.google.com/p/feedparser/source/browse/trunk/feedparser/feedparser.py)
        # if feed is gzip-compressed, decompress it
        if gzip and resp.headers.getheader('content-encoding', None) == 'gzip':
            try:
                resp_data = gzip.GzipFile(fileobj = StringIO(resp_data)).read()
            except (IOError, struct.error), e:
                # IOError can occur if the gzip header is bad
                # struct.error can occur if the data is damaged
                # Some feeds claim to be gzipped but they're not, so
                # we get garbage.  Ideally, we should re-request the
                # feed without the 'Accept-encoding: gzip' header,
                # but we don't.
                pass
        elif zlib and resp.headers.getheader('content-encoding', None) == 'deflate':
            try:
                resp_data = zlib.decompress(resp_data)
            except zlib.error, e:
                pass
                
    return (resp, cookiejar, resp_data)

def buildcookie(uin, skey):
    '''
    return a cookiejar with login state for uin.
    '''
    cj = cookielib.CookieJar()
    ck = cookielib.Cookie(version = 0, name = 'uin', value = 'o%s' % uin, port = None,
                           port_specified = False, domain = 'qq.com',
                           domain_specified = False, domain_initial_dot = False, path = '/',
                           path_specified = True, secure = False, expires = None,
                           discard = True, comment = None, comment_url = None,
                           rest = {'HttpOnly': None}, rfc2109 = False)
    ck2 = cookielib.Cookie(version = 0, name = 'skey', value = skey, port = None,
                           port_specified = False, domain = 'qq.com',
                           domain_specified = False, domain_initial_dot = False, path = '/',
                           path_specified = True, secure = False, expires = None,
                           discard = True, comment = None, comment_url = None,
                           rest = {'HttpOnly': None}, rfc2109 = False)
    cj.set_cookie(ck)
    cj.set_cookie(ck2)
    return cj

def parse_request_from_file(path):
    '''
    parse request from file
    '''
    raw_http = open(path).read()
    # if your are reading a text file from windows, u may need manually convert \n to \r\n
    # universal newline support: http://docs.python.org/library/functions.html#open
    raw_http = raw_http.replace('\n', '\r\n')
    p = HttpParser()
    p.execute(raw_http, len(raw_http))
    return p

if __name__ == '__main__':
    x=urlopen(r'http://localhost/40236')
    print x
    print x[0].getcode()
