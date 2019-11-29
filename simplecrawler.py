#!/usr/bin/env python3
# encoding: utf-8
import socket
import json
import argparse
import logging


class Error(Exception):

    """Yggdrasil API error"""

    def __str__(self):
        return self.__class__.__name__ + ': ' + ' '.join(self.args)


def doRequest(req):
    if hasattr(socket, 'AF_UNIX'):
        ygg = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        ygg.connect('/var/run/yggdrasil.sock')
    else:
        ygg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ygg.connect(('localhost', 9001))
    try:
        ygg.send(json.dumps(req).encode())
        data = json.load(ygg.makefile(encoding='utf-8'))
    finally:
        ygg.close()
    if data['status'] == 'error':
        raise Error(data.get('error'))
    return data.get('response')


def getnodesrec(pubkey=None, coords=None, skip=set()):
    if pubkey is None:
        node = list(doRequest({"request": "getself"})['self'].values())[0]
        pubkey = node['box_pub_key']
        coords = node['coords']
        yield (pubkey, coords)
    if pubkey not in skip:
        skip.add(pubkey)
        logging.info((pubkey, coords, len(skip)))
        try:
            dht = doRequest({"request": "dhtPing",
                             "box_pub_key": pubkey, "coords": coords})
            for node in dht['nodes'].values():
                for (k, c) in getnodesrec(node['box_pub_key'], node['coords'],
                                          skip):
                    yield (k, c)
                    skip.add(k)
        except Error:
            pass


def getnodesinfo(nodes):
    for k, c in nodes:
        try:
            info = doRequest({"request": "getNodeInfo",
                              "box_pub_key": k, "coords": c})
            yield (k, info.get('nodeinfo'))
        except Error:
            yield (k, {})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get nodeinfo from all nodes')
    parser.add_argument('target', type=argparse.FileType('w'), nargs=1)
    parser.add_argument('-v', action='store_true')
    p = parser.parse_args()
    if p.v:
        logging.basicConfig(level=logging.INFO)
    try:
        allnodes = {k: v for (k, v) in getnodesinfo(getnodesrec())}
    finally:
        json.dump(allnodes, p.target[0], sort_keys=True, indent=2)
