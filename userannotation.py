#-*- coding: utf-8 -*-

from tetpyclient import RestClient
import tetpyclient
import pprint
import json
import argparse
import os
import urllib3

urllib3.disable_warnings()
API_ENDPOINT="https://tetration-cluster-endpoint"


restclient = RestClient(API_ENDPOINT,
                credentials_file='api_all.json',
                verify=False)

file_path = 'test.csv' # source file contains hangul with UTF-8 encoding
app_scope = 'APJDemo' # name of scope  VRF independent 

# upload user annotation file 
req_payload = [tetpyclient.MultiPartOption(key='X-Tetration-Oper', val='add')]
resp = restclient.upload(file_path, '/assets/cmdb/upload/' + app_scope, req_payload)
print( resp, resp.text)

file_path = 'output.csv'
resp = restclient.download(file_path, '/assets/cmdb/download/' + app_scope)

# activate annotation with column names 
req_payload = ['VM_Name', 'VM_Guest_OS', 'VM_Host', 'VM_Datastore', 'VM_Network', "VM_OWNER"]
resp = restclient.put('/assets/cmdb/annotations/' + app_scope, json_body=json.dumps(req_payload))
print( resp, resp.text)

