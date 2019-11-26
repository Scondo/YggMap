'''
Created on 20 нояб. 2019 г.

@author: scond
'''
from simplecrawler import getnodesinfo, getnodesrec
import json
import time


keptnodes = {}
try:
    keptnodes = json.load(open("nodes.json", 'r'))
except FileNotFoundError:
    keptnodes = {}
allnodes = getnodesinfo(getnodesrec())
freshnodes = {}
for k, v in allnodes:
    if (v is not None and 'physical' in v and
            'coord' in v['physical'] and 'SSID' in v['physical']):
        freshnodes[k] = {"lastseen": time.time(), "physical": v['physical'],
                         'contact': v.get('contact', '')}
    elif k in keptnodes:  # When someone removes his location from nodeinfo
        del keptnodes[k]
keptnodes.update(freshnodes)
json.dump(keptnodes, open("nodes.json", 'w'), sort_keys=True, indent=2)
