#coding=utf-8
'''
Created on 2012-7-8

@author: fengclient
'''
#beautiful soup 3
from BeautifulSoup import BeautifulSoup
from urllib2 import urlparse

def is_index(soup):
    return True if soup.find(id='list_wapper') else False

def is_page(soup):
    return True if soup.find(id='test_data') else False

def find_pics(soup,url):
    title=unicode(soup.find(id='test_head_t').h1.string)
    pic_tags=soup.find(id='test_data').findAll('img')
    pic_urls=[urlparse.urljoin(url,img['src']) for img in pic_tags]
    return title,pic_urls

def find_next_pages(soup,url):
    a_tags=soup.find(id='test_data').nextSibling.div.findAll('a')
    page_urls=[urlparse.urljoin(url,a['href']) for a in a_tags]
    return page_urls

def find_pages_from_index(soup,url):
    a_tags=soup.find(id='list_wapper').findAll('a')
    return [urlparse.urljoin(url,a['href']) for a in a_tags]

def find_next_indexes(soup,url):
    a_tags=soup.find(id='list_wapper').parent.find(attrs={'class':'test_page'}).findAll('a')
    index_urls=[urlparse.urljoin(url,a['href']) for a in a_tags]
    return index_urls

def find_recommendations(html_doc,url):
    pass

if __name__ == '__main__':
    pass
    