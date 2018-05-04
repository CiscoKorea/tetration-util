#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tetpyclient import RestClient
import sys, os, json, getopt
import csv
import traceback
from tetpyclient import RestClient
from tetpyclient import MultiPartOption
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

API_ENDPOINT="https://medusa-cpoc.cisco.com"


def get_scope_id( client, scope_name):
    scope_id = None
    resp = client.get('/openapi/v1/app_scopes')
    #print( resp, resp.text)
    if resp.status_code == 200:
        scopes = json.loads( resp.text)
        for scope in scopes:
            if scope['name'] == scope_name:
                print( "{0} {1} matched".format( scope['name'], scope['id']))
                scope_id = scope['id']
                break
        return scope_id
    else:
        return None


def upload_server_port_config(endpoint, file_path, scope_name):

    restclient = RestClient(endpoint,
                    credentials_file='api_key.json',
                    verify=False)

    scope_id = get_scope_id( restclient, scope_name)
    if scope_id is not None and os.path.exists(file_path) :
        req_payload = [MultiPartOption(key='X-Tetration-Oper', val='add')]
        resp = restclient.upload(file_path,
                    '/openapi/v1/adm/{0}/server_ports'.format(scope_id),
                    req_payload,
                    timeout=200) # seconds

        print(resp, resp.text)
    else:
        print('Wrong scope name {0} or server ports config file {1} does not exist'.format( scope_name, file_path))
    

if __name__ == '__main__':
    endpoint, infile, scope = (None,None,None)
    myopts, args = getopt.getopt(sys.argv[1:],"h:i:s:")
    for o, a in myopts:
        if o == '-h':
            endpoint = a
        elif o == '-i':
            infile = a
        elif o == '-s':
            scope = a
        else:
            print("Usage : {0} -h {{https://tetration-cluster-ipaddr}} -i {{server_port_conf_file}} -s {{scope_name}}".format( sys.argv[0]))
            sys.exit(0)
    if endpoint and infile and scope :
       upload_server_port_config( endpoint, infile, scope)
    else:
       print("Usage : {0} -h {{https://tetration-cluster-ipaddr}} -i {{server_port_conf_file}} -s {{scope_name}}".format( sys.argv[0]))