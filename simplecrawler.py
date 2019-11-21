#!/usr/local/bin/python3.6
# encoding: utf-8
import socket
import json
import argparse


class Error(Exception):

    """Yggdrasil API error"""

    def __str__(self):
        return self.__class__.__name__ + ': ' + ' '.join(self.args)


def doRequest(req):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ygg:
        ygg.connect(('localhost', 9001))
        ygg.send(json.dumps(req).encode())
        data = json.load(ygg.makefile(encoding='utf-8'))
        if data['status'] == 'error':
            raise Error(data.get('error'))
    return data.get('response')


def getrecursive(pubkey=None, coords=None, skip=set()):
    if pubkey is None:
        node = list(doRequest({"request": "getself"})['self'].values())[0]
        pubkey = node['box_pub_key']
        coords = node['coords']
    if pubkey not in skip:
        print (pubkey, coords, len(skip))
        try:
            info = doRequest({"request": "getNodeInfo",
                              "box_pub_key": pubkey, "coords": coords})
            yield (pubkey, info.get('nodeinfo'))
        except Error:
            yield (pubkey, {})

        try:
            dht = doRequest({"request": "dhtPing",
                             "box_pub_key": pubkey, "coords": coords})
            for node in dht['nodes'].values():
                res0 = getrecursive(node['box_pub_key'], node['coords'],
                                    skip)
                for (k, v) in res0:
                    yield (k, v)
                    skip.add(k)
        except Error:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get nodeinfo from all nodes')
    parser.add_argument('target', type=argparse.FileType('w'), nargs=1)
    p = parser.parse_args()
    try:
        allnodes = {k: v for (k, v) in getrecursive()}
    finally:
        json.dump(allnodes, p.target[0], sort_keys=True, indent=2)
