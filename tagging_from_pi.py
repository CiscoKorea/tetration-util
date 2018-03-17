#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, requests
import sys, getopt
from sets import Set
#
#
#   device - deviceInterface - clients 
#   device - vlan - client 
#
#
#
#

#PI api information 
PI_API_ENDPOINT = 'https://10.72.80.169/'
USER_NAME = 'root'
USER_PASSWD = '1234Qwer'
PAGE_SIZE = 100
FULL_DESC = 'true'

clientsMaps = {}
def get_all_clients( api_path):
    global PAGE_SIZE
    clients = {} 
    path = "{0}.{1}?.full=true&.maxResults={2}&.firstResult={3}".format( api_path, 'json', PAGE_SIZE, 0)
    get_resp = requests.get( PI_API_ENDPOINT + path, auth=(USER_NAME,USER_PASSWD), verify=False)
    if get_resp.status_code != 200:
        return []
    resp = json.loads( get_resp.text)
    count = int(resp['queryResponse']['@count'])
    first = int(resp['queryResponse']['@first'])
    last = int(resp['queryResponse']['@last'])
    #print( "count={0}, first={1} and last={2}".format( count, first, last))
    PAGE_SIZE = last - first + 1 if last - first + 1 < PAGE_SIZE  else PAGE_SIZE
    for entry in resp['queryResponse']['entity']:
        clients[ entry['clientsDTO']['@id']] = entry['clientsDTO']

    while last + 1 != count:
        print('loop count with last=%d' %(last+1))
        path = "{0}.{1}?.full=true&.maxResults={2}&.firstResult={3}".format( api_path, 'json', PAGE_SIZE, last+1)
        get_resp = requests.get( PI_API_ENDPOINT + path, auth=(USER_NAME,USER_PASSWD), verify=False)
        if get_resp.status_code != 200:
            return clients 
        resp = json.loads( get_resp.text)
        count = int(resp['queryResponse']['@count'])
        #first = int(resp['queryResponse']['@first'])
        last = int(resp['queryResponse']['@last'])
        for entry in resp['queryResponse']['entity']:
            clients[ entry['clientsDTO']['@id']] = entry['clientsDTO']
    return clients

def get_client_detail( api_path, client_id):
    path = "{0}/{1}.{2}".format( api_path, client_id, 'json')
    get_resp = requests.get( PI_API_ENDPOINT + path, auth=(USER_NAME,USER_PASSWD), verify=False)
    if get_resp.status_code != 200:
        return {} 
    resp = json.loads( get_resp.text)
    client_dto = resp['queryResponse']['entity']['clientsDTO']
    return client_dto

def get_clients_per_device_intf( clients):
    device_names = {}
    devices = {}
    for client_id in clients:
        try:
            ipaddr = clients[client_id]['deviceIpAddress']['address']
            if not devices.has_key( ipaddr):
                devices[ ipaddr] = { 'intf': {}, 'vlan': {}, 'vendor': [],'name': None}
            if clients[client_id]['status'] == 'ASSOCIATED':
                device_names[ ipaddr ] = clients[client_id]['deviceName'] + '/' + clients[client_id]['vendor']
            devices[ipaddr]['name'] = clients[client_id]['deviceName']
            if not clients[client_id]['vendor'] in devices[ipaddr]['vendor'] :
                devices[ipaddr]['vendor'].append( clients[client_id]['vendor'])
            intf = clients[client_id]['clientInterface']
            if not devices[ipaddr]['intf'].has_key( intf):
                devices[ipaddr]['intf'][intf] = []
            devices[ipaddr]['intf'][intf].append(clients[client_id]['ipAddress']['address'])
            vlan = clients[client_id]['vlanId']
            if not devices[ipaddr]['vlan'].has_key( vlan):
                devices[ipaddr]['vlan'][vlan] = []
            devices[ipaddr]['vlan'][vlan].append(clients[client_id]['ipAddress']['address'])
            #print( intf,clients[client_id]['ipAddress']['address'] )
        except KeyError as ke:
            pass
    return (devices)

def get_clients_per_device_vlan( clients):
    pass

def conv_inventory_format( clients):
    inventory = {}
    for device_ipaddr in clients:
        for phys_intf in clients[device_ipaddr]['intf']:
            eps = clients[device_ipaddr]['intf'][phys_intf]
            ipaddr = None
            for ep in eps:
                ipaddr = ep
                if ep not in inventory:
                    inventory[ep] = {}
                item = inventory[ep]
                item['deviceName'] = clients[device_ipaddr]['name'] 
                item['devicePhysIntf'] = phys_intf
            if ipaddr:
                inventory[ipaddr] = item
        for vlan in clients[device_ipaddr]['vlan']: 
            eps = clients[device_ipaddr]['vlan'][vlan] 
            ipaddr = None
            for ep in eps:
                ipaddr = ep
                if ep not in inventory:
                    inventory [ ep ] = {}
                item = inventory[ep]
                item['deviceName'] = clients[device_ipaddr]['name'] 
                item['deviceVlan'] = vlan
            if ipaddr:
                inventory[ipaddr] = item
    return inventory


def get_all_neighborhoods(api_path):
    global PAGE_SIZE
    neighborhoods = {} 
    path = "{0}.{1}?.full=true&.maxResults={2}&.firstResult={3}".format( api_path, 'json', PAGE_SIZE, 0)
    get_resp = requests.get( PI_API_ENDPOINT + path, auth=(USER_NAME,USER_PASSWD), verify=False)
    if get_resp.status_code != 200:
        return []
    resp = json.loads( get_resp.text)
    count = int(resp['queryResponse']['@count'])
    first = int(resp['queryResponse']['@first'])
    last = int(resp['queryResponse']['@last'])
    #print( "count={0}, first={1} and last={2}".format( count, first, last))
    PAGE_SIZE = last - first + 1 if last - first + 1 < PAGE_SIZE  else PAGE_SIZE
    for entry in resp['queryResponse']['entity']:
        if entry['inventoryDetailsDTO']['@id'] not in neighborhoods:
           neighborhoods[entry['inventoryDetailsDTO']['@id']] = { 'summary':{}, 'cdpNeighbors': {} }
        if 'cdpNeighbors' in entry['inventoryDetailsDTO']:
            neighborhoods[ entry['inventoryDetailsDTO']['@id']]['cdpNeighbors'] = entry['inventoryDetailsDTO']['cdpNeighbors']
        neighborhoods[ entry['inventoryDetailsDTO']['@id']]['summary'] = entry['inventoryDetailsDTO']['summary'] 

    while last + 1 != count:
        #print('loop count with last=%d' %(last+1))
        path = "{0}.{1}?.full=true&.maxResults={2}&.firstResult={3}".format( api_path, 'json', PAGE_SIZE, last+1)
        get_resp = requests.get( PI_API_ENDPOINT + path, auth=(USER_NAME,USER_PASSWD), verify=False)
        if get_resp.status_code != 200:
            return clients 
        resp = json.loads( get_resp.text)
        count = int(resp['queryResponse']['@count'])
        #first = int(resp['queryResponse']['@first'])
        last = int(resp['queryResponse']['@last'])
        for entry in resp['queryResponse']['entity']:
            if entry['inventoryDetailsDTO']['@id'] not in neighborhoods:
                neighborhoods[entry['inventoryDetailsDTO']['@id']] = { 'summary':{}, 'cdpNeighbors': {} }
            if 'cdpNeighbors' in entry['inventoryDetailsDTO']:
                neighborhoods[ entry['inventoryDetailsDTO']['@id']]['cdpNeighbors'] = entry['inventoryDetailsDTO']['cdpNeighbors']
            neighborhoods[ entry['inventoryDetailsDTO']['@id']]['summary'] = entry['inventoryDetailsDTO']['summary'] 
    return neighborhoods
    
def gen_visdata_from_neighborhoods( val):
    visData = { 'nodes': [], 'edges': [], 'options': {}}
    name_to_id = {}
    for inv_id in val:
        node = {}
        node['id'] = inv_id
        if 'deviceName' in val[inv_id]['summary']:
            node['label'] = val[inv_id]['summary']['deviceName']
            name_to_id[ node['label']] = inv_id
        else:
            node['label'] = 'Unknown'
        node['title'] = '<ul>'
        if 'ipAddress' in val[inv_id]['summary']:
            node['title'] = node['title'] + '<li>IP: ' + val[inv_id]['summary']['ipAddress'] +'</li>'
        if 'deviceType' in val[inv_id]['summary']:
            node['title'] = node['title'] + '<li>Type: ' + val[inv_id]['summary']['deviceType'] +'</li>'
        node['title'] = node['title'] + '</ul>'
        node['shape'] = 'box'
        visData['nodes'].append( node)
    for inv_id in val:
        edge = {}
        if 'cdpNeighbor' in val[inv_id]['cdpNeighbors']:
            for neighbor in val[inv_id]['cdpNeighbors']['cdpNeighbor']:
                if name_to_id.has_key(neighbor['neighborDeviceName']):
                    neighbor_id =  name_to_id[neighbor['neighborDeviceName']]
                    edge['from'] = inv_id
                    edge['to'] = neighbor_id
                    edge['arrow'] = 'to'
                    edge['label'] = neighbor['farEndInterface']
        if len(edge) > 0:
            visData['edges'].append( edge)
    return visData



if __name__ == '__main__':
    clients = get_all_clients ( '/webacs/api/v3/data/Clients')
    #print( json.dumps(clients))
    devices = get_clients_per_device_intf( clients)
    print( json.dumps( conv_inventory_format(devices)))
    neighborhoods = get_all_neighborhoods('/webacs/api/v3/data/InventoryDetails')
    #print( json.dumps(neighborhoods))
    visdata = gen_visdata_from_neighborhoods(neighborhoods)
    #print( json.dumps( visdata))
    #print( json.dumps(devices))


