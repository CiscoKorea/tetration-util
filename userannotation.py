#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tetpyclient import RestClient
import tetpyclient
import pprint
import json
import argparse
import os
import urllib3
import sys, getopt

urllib3.disable_warnings()

def upload_userdata( endpoint, file_path, app_scope):
    restclient = RestClient(endpoint,
                    credentials_file='api_key.json',
                    verify=False)

    #file_path = # source file contains hangul with UTF-8 encoding
    #app_scope = 'APJDemo' # name of scope  VRF independent 

    # upload user annotation file 
    req_payload = [tetpyclient.MultiPartOption(key='X-Tetration-Oper', val='add')]
    resp = restclient.upload(file_path, '/assets/cmdb/upload/' + app_scope, req_payload)
    #print(resp, resp.text)

    #file_path = 'output.csv'
    #resp = restclient.download(file_path, '/assets/cmdb/download/' + app_scope)

    with open(file_path) as inf:
        # activate annotation with column names 
        # hdr = ['VM_Name', 'VM_Guest_OS', 'VM_Host', 'VM_Datastore', 'VM_Network', "VM_OWNER"]
        hdr = inf.readline().strip().split(',')
        print(hdr[1:])
        resp = restclient.put('/assets/cmdb/annotations/' + app_scope, json_body=json.dumps(hdr[1:]))
        print(resp, resp.text)

if __name__ == '__main__':
    endpoint, inventory, scope = (None,None,None)
    myopts, args = getopt.getopt(sys.argv[1:],"h:i:s:")
    for o, a in myopts:
        if o == '-h':
            endpoint = a
        elif o == '-i':
            inventory = a
        elif o == '-s':
            scope = a
        else:
            print("Usage : {0} -h {{https://tetration-cluster-ipaddr}} -i {{inventory_file}} -s {{scope_name}}".format( sys.argv[0]))
            sys.exit(0)
    if endpoint and inventory and scope :
       upload_userdata( endpoint, inventory, scope)
    else:
       print("Usage : {0} -h {{https://tetration-cluster-ipaddr}} -i {{inventory_file}} -s {{scope_name}}".format( sys.argv[0]))
