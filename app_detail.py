#-*- coding: utf-8 -*-
# 
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
# credentials.json looks like:
# {
#   "api_key": "<hex string>",
#   "api_secret": "<hex string>"
# }

def convert_policy_to_csv( infile, outfile):
    with open( infile, "r") as inf:
        appbody = json.loads( inf.read())
        hostmap = {}
        server_list_file = ''
        if appbody['name'].startswith('dfs'):
            server_list_file = 'dfs'
        elif appbody['name'].startswith('starbucks'):
            server_list_file = 'starbucks'
        with open( server_list_file + '_server_list.csv', 'r') as mapf:
            lines = mapf.read()
            for line in lines.split('\r'):
                items = line.strip().split(',')
                hostmap[ items[0]] = { 'mode': items[1], 'hostname': items[2]}
        with open("{0}-App-{1}.csv".format(appbody['name'], appbody['version']), "w+") as outf:
            outf.write("App_Name, Cluster_Name, Endpoint_IP, Hostname\n")
            if not appbody.has_key( 'clusters'):
                continue
            for cluster in appbody['clusters']:
                ips = ""
                first_ips = True
                for endpoint in cluster['nodes']:
                    #ips = ips + "\t- {0}\n".format( endpoint['ip'])
                    if first_ips:
                        ips = "{0}, {1}, {2},{3}/{4}\n".format( app['name'], cluster['name'], endpoint['ip'], hostmap.get(endpoint['ip'], {'hostname':'none'}).get('hostname', 'none'), hostmap.get(endpoint['ip'], {'mode':'prod'}).get('mode') )
                        first_ips = False
                    else: 
                        ips = ", , {0},{1}/{2}\n".format( endpoint['ip'], hostmap.get(endpoint['ip'], {'hostname':'none'}).get('hostname', 'none'), hostmap.get(endpoint['ip'], {'mode':'prod'}).get('mode') )
                    outf.write(ips)
        print("{0}-App-{1}.csv is generated...".format(appbody['name'], appbody['version']))

if __name__ == '__main__':
    # Read command line args
    infile = None
    outfile = None
    myopts, args = getopt.getopt(sys.argv[1:],"i:")
    for o, a in myopts:
        if o == '-i':
            infile = a
        else:
            print("Usage : {0} -i input_app_policy_json -o output_csv ".format( sys.argv[0]))
            sys.exit(0)
    if infile  and outfile:
        print("input file {0}, and output file {1}".format( infile, outfile))
        convert_policy_to_csv( infile, outfile)
    else:
        print("Usage : %s -i input_app_policy_json -o output_csv".format( sys.argv[0]))
        sys.exit(0)