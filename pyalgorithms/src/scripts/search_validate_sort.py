'''
Created on 2012-3-21

@author: fengclient
'''
import json
from argparse import ArgumentParser

def check(filepath):
    f=open(filepath,'r')
    jsondata=json.loads(unicode(f.read(),'utf8'))
    id_mapinfo_pairs=[(e['grouponId'],e['mapInfo'] if e.has_key('mapInfo') else None) for e in jsondata["data"]["lists"]]
    for (id,map) in id_mapinfo_pairs:
        print id,map

if __name__ == '__main__':
    parser = ArgumentParser(description = 'dump location info from json text from search')
    parser.add_argument('input', nargs = 1, metavar = '<json text file>')
    ns = parser.parse_args()
    a = check(ns.input[0])