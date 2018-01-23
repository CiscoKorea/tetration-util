#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json 
import sys, getopt

slb_conf = {}
slb_conf['configs'] = []

def conv_to_l4_json( src, dst):
    with open( src, 'r') as inf:
        for line in inf.readlines():
            if skip_header: # just skip first header row
                skip_header = False
                continue
            line = line.strip()
            items = line.split(",")
            name = items[0]
            for port in items[2].split():
                l4_entry = {}
                l4_entry['protocol'] = 6 # TCP 
                l4_entry['name'] = name + '-' + port
                l4_entry['vip'] = items[1]
                l4_entry['vip_port'] = int(port)
                backends = []
                for bip in items[3].split():
                    backends.append( {'backend_ip': bip, 'backend_port': int(port)})
                l4_entry['backends'] = backends
                slb_conf['configs'].append( l4_entry)
    with open( dst, 'w+') as outf:
        outf.write( json.dumps( slb_conf))



if __name__ == '__main__':
    # Read command line args
    infile = None
    outfile = None
    myopts, args = getopt.getopt(sys.argv[1:],"i:o:")
    for o, a in myopts:
        if o == '-i':
            infile = a
        elif o == '-o':
            outfile = a
        else:
            print("Usage : {0} -i input -o output ".format( sys.argv[0]))
            sys.exit(0)
    if infile  and outfile:
        print("input file {0}, and output file {1}".format( infile, outfile))
        conv_to_l4_json( infile, outfile)
    else:
        print("Usage : %s -i input -o output ".format( sys.argv[0]))
        sys.exit(0)
