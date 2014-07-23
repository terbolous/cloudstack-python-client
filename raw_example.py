import urllib2
import urllib
import hashlib
import hmac
import base64
#from lxml import etree

import json
#from peewee import *
from pprint import pprint


#class DbVolumns(Model):
#    instance_id = CharField()
#    name = CharField()
#    path = CharField()


import MySQLdb

host_str='172.16.206.143'

#db = peewee.MySQLDatabase("cloud", host="", user="root", passwd="password")
#print db

db = MySQLdb.connect(host=host_str, # your host, usually localhost
                     user="root", # your username
                      passwd="password", # your password
                      db="cloud") # name of the data base
cur = db.cursor()



import MySQLdb



def get_request_url(command_str , args ):
    baseurl='http://172.16.206.143:8080/client/api?'
    request={}
    #request['command']='listUsers'
    #below is private api under cloudstack 4.0.2
    #request['command']='createVMSnapshot'
    #request['vmid']='50e9dbdd-2efe-4df0-8478-581fd43088ce'
    request['command'] = command_str
    if args is not None:
        for k,v in args.iteritems():
            request[k]=v
    #request['response']='xml'
    request['response']='json'
    request['apikey']='FhlHSpLcOEiB8wVI6xXH8XfA9nLGzdim5eVlUsVa9LXDIleqsAJA1yubYrEHCduSSsCur6gVoEUmQFctHgxv1g'
    secretkey='YbftfeOwmC3uBvQfYgSXUwkuUuMeca6G7EKvUZJFeZrivjpFwEMGZlXMqn3rCt0YRy9mPtyt-1F2S9s0IFBqKQ'
    request_str='&'.join(['='.join([k,urllib.quote_plus(request[k])]) for k in request.keys()])
    sig_str='&'.join(['='.join([k.lower(),urllib.quote_plus(request[k].lower().replace('+','%20'))])for k in sorted(request.iterkeys())])
    sig=hmac.new(secretkey,sig_str,hashlib.sha1)
    sig=hmac.new(secretkey,sig_str,hashlib.sha1).digest()
    sig=base64.encodestring(hmac.new(secretkey,sig_str,hashlib.sha1).digest())
    sig=base64.encodestring(hmac.new(secretkey,sig_str,hashlib.sha1).digest()).strip()
    sig=urllib.quote_plus(base64.encodestring(hmac.new(secretkey,sig_str,hashlib.sha1).digest()).strip())
    req=baseurl+request_str+'&signature='+sig
    return req



def get_json_result(req_str,args):
    req = get_request_url( req_str , args )
    res=urllib2.urlopen(req)
    result_json = res.read()
    return result_json



def get_volumns_info(vm_id):
    #listVolumes
    args={}
    args['virtualmachineid'] = vmid
    command_str = "listVolumes"
    result_json = get_json_result(command_str,args)
    return result_json



def get_vmid_by_disp_name(vm_name):
    #print req
    args={}
    command_str = "listVirtualMachines"
    result_json = get_json_result(command_str,args)

    #print result_json

    #print json.dumps( result_json , sort_keys=True,   indent=4, separators=(',', ': '))


    obj_listvm = json.loads(result_json)

    #print obj_listvm['listvirtualmachinesresponse']['count']
    obj_vms= obj_listvm['listvirtualmachinesresponse']['virtualmachine']

    for vm in obj_vms:
        if vm['displayname'] not in vm_name:
            continue
        #print vm['domainid']
        #print vm['zoneid']
        #print vm['instancename']
        #print vm['id']
        #print vm['displayname']
        return vm['id']
        break
    return None



vm_name='i-2-5-VM'
vmid=get_vmid_by_disp_name(vm_name)
if vmid is not None:
    #print 'vmid=',vmid
    result_json = get_volumns_info(vmid)
    obj_volumns = json.loads(result_json)
    obj_volumns= obj_volumns['listvolumesresponse']['volume']
    for one_vol in obj_volumns:
        print one_vol['name']
        # Use all the SQL you like
        cur.execute("SELECT name,path FROM volumes where 1=1 and name = '"+ one_vol['name'] +"' ")
        # print all the first cell of all the rows
        for row in cur.fetchall() :
            vhd_file_uuid_in_primary_store = row[1]
            #send to s3








#root = etree.fromstring(result)
#print etree.tostring(root, pretty_print=True)




