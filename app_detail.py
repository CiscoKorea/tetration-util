#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tetpyclient import RestClient
import pprint
import json
import sys, getopt

# ``verify`` is an optional param to disable SSL server authentication.
# By default, Tetration appliance dashboard IP uses self signed cert after
# deployment. Hence, ``verify=False`` might be used to disable server
# authentication in SSL for API clients. If users upload their own
# certificate to Tetration appliance (from ``Settings > Company`` Tab)
# which is signed by their enterprise CA, then server side authentication
# should be enabled.
# api_key.json looks like:
# {
#   "api_key": "<hex string>",
#   "api_secret": "<hex string>"
# }


def get_app_detail( endpoint):
    restclient = RestClient(endpoint,
                    credentials_file='api_key.json',
                    verify=False)

    apps = []
    resp = restclient.get('/applications')
    if resp.status_code == 200 :
        respbody = json.loads(resp.text)
        for app in respbody:
            appnames = {}
            appnames['id'] = str(app['id'])
            appnames['name'] = app['name']
            appnames['version'] = str(app['version'])
            apps.append( appnames)
    else:
        print( resp, resp.text)


    for app in apps:
        hostmap = {}
        server_list_file = app['name']
        try:
            with open( server_list_file + '_server_list.csv', 'r') as mapf:
                lines = mapf.read()
                for line in lines.split('\r'):
                    items = line.strip().split(',')
                    hostmap[ items[0]] = { 'mode': items[1], 'hostname': items[2]}
        except Exception as error:
            print('No matching server list file')
        resp = restclient.get('/applications/%s/details' %(app['id']))
        if resp.status_code == 200:
            with open('%s-App-%s.csv' %(app['name'], app['version']), "w+") as outf:
                outf.write("Cluster_ID, Cluster_Name, New_Cluster_Name, Endpoint_IP, Hostname\n")
                appbody = json.loads(resp.text)
                if not appbody.has_key( 'clusters'):
                    continue
                for cluster in appbody['clusters']:
                    ips = ""
                    first_ips = True
                    for endpoint in cluster['nodes']:
                        if first_ips:
                            ips = "{0}, {1}, , {2},{3}/{4}\n".format( cluster['id'], cluster['name'], endpoint['ip'], hostmap.get(endpoint['ip'], {'hostname':'none'}).get('hostname', 'none'), hostmap.get(endpoint['ip'], {'mode':'none'}).get('mode') )
                            first_ips = False
                        else:
                            ips = ", , , {0},{1}/{2}\n".format( endpoint['ip'], hostmap.get(endpoint['ip'], {'hostname':'none'}).get('hostname', 'none'), hostmap.get(endpoint['ip'], {'mode':'none'}).get('mode') )
                        outf.write(ips)


if __name__ == '__main__':
    endpoint = None
    myopts, args = getopt.getopt(sys.argv[1:],"h:")
    for o, a in myopts:
        if o == '-h':
            endpoint = a
        else:
            print("Usage : {0} -h https://{{tetration-cluster-ipaddr}}".format( sys.argv[0]))
            sys.exit(0)
    if endpoint :
       get_app_detail(endpoint)
    else:
       print("Usage : {0} -h https://{{tetration-cluster-ipaddr}}".format( sys.argv[0]))