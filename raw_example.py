import urllib2
import urllib
import hashlib
import hmac
import base64
#from lxml import etree

import json

import peewee
from peewee import *

from pprint import pprint

import MySQLdb



from  AWSS3 import uploader




uploader.help_s3()

uploader.test()

exit()



class DbVolumns(Model):
    instance_id = CharField()
    name = CharField()
    path = CharField()



host_str='XXX.XXX.XXX.XXX'

if False:
    db = peewee.MySQLDatabase("cloud", host=host_str, user="root", passwd="password")
    print "peewee"
    print db
    print "end"
else:
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

    request['apikey']=''
    secretkey=''

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



def get_snapshots(volumn_id):
    args={}
    args['volumnid']=volumn_id
    command_str='listSnapshots'
    result_json = get_json_result(command_str,args)
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


def get_vm_template_id(vm_id):
    cur.execute("SELECT vm_template_id FROM vm_instance where 1=1 and uuid = '"+ vm_id +"' ")
    rows = cur.fetchall()
    if 1 != len(rows):
        print "Error when get vm_template_id of :", vm_id
        exit()
    else:
        return rows[0][0]


def get_vm_instance_id(vm_id):
    cur.execute("SELECT id FROM vm_instance where 1=1 and uuid = '"+ vm_id +"' ")
    rows = cur.fetchall()
    if 1 != len(rows):
        print "Error when get vm instance id of :", vm_id
        exit()
    else:
        return rows[0][0]


def get_vm_template_vhd_uuid(vm_tmplt_id):
    cur.execute("SELECT unique_name FROM vm_template where 1=1 and id = "+ str(vm_tmplt_id) +" ")
    rows = cur.fetchall()
    if 1 != len(rows):
        print "Error when get vm template uuid of :", vm_tmplt_id
        exit()
    else:
        return rows[0][0]


def get_vm_volumn_id(instance_id):
    cur.execute("SELECT id FROM volumes where 1=1 and instance_id = "+ str(instance_id) +" ")
    rows = cur.fetchall()
    if 1 != len(rows):
        print "Error when get vm volumn id of instance id:", instance_id
        exit()
    else:
        return rows[0][0]


def get_vm_folder_path(instance_id):
    cur.execute("SELECT folder,path FROM volumes where 1=1 and instance_id = "+ str(instance_id) +" ")
    rows = cur.fetchall()
    if 1 != len(rows):
        print "Error when get vm volumn id of instance id:", instance_id
        exit()
    else:
        return rows[0][0],rows[0][1]


def get_snapshot_info(volume_id):
    print "FOR DEBUG , SO ONLY GET THE LASTEST ONE "
    cur.execute("SELECT account_id,status,backup_snap_id FROM snapshots where 1=1 and volume_id = "+ str(volume_id) +" ORDER BY id DESC LIMIT  1 ")
    rows = cur.fetchall()
    if 1 != len(rows):
        print "Error when get vm snapshot id of instance id:", instance_id
        exit()
    else:
        if rows[0][1] == "BackedUp":
            return rows[0][0],rows[0][2]
        else:
            print " the snapshot is not successed , so can not continue."
            exit()







vm_name='i-2-6-VM'
print "PLEASE CHECK YOUR VM NAME:", vm_name
vmid=get_vmid_by_disp_name(vm_name)
if vmid is not None:
    #print "vmid of ", vm_name, " is ", vmid
    vm_template_id = get_vm_template_id(vmid)
    #print "vm_template_id of ", vm_name, " is ", vm_template_id
    vm_tmplt_uuid = get_vm_template_vhd_uuid(vm_template_id)

    #print "vm tmplt uuid is:", vm_tmplt_uuid
    print "/home/export/secondary/template/tmpl/2/"+str(vm_template_id)+"/"+ vm_tmplt_uuid
    #///home/export/secondary/template/tmpl/2/204/

    instance_id = get_vm_instance_id(vmid)
    folder,path_volumn = get_vm_folder_path(instance_id)

    print "folder is :", folder+"/"+path_volumn
    #print "path is :", path_volumn
    volume_id = get_vm_volumn_id(instance_id)
    account_id , snap_id = get_snapshot_info( volume_id )
    #print "account id is :", account_id
    #print "snap_id is ", snap_id
    print "/home/export/secondary/snapshots/"+str(account_id)+"/"+str(volume_id)+"/"+snap_id
    #print 'vmid=',vmid


    exit()
    result_json = get_volumns_info(vmid)
    obj_volumns = json.loads(result_json)
    obj_volumns= obj_volumns['listvolumesresponse']['volume']
    for one_vol in obj_volumns:
        print one_vol['name']
        # Use all the SQL you like
        cur.execute("SELECT name,path FROM volumes where 1=1 and name = '"+ one_vol['name'] +"' ")
        # print all the first cell of all the rows
        rows = cur.fetchall()
        for row in rows:
            vhd_file_uuid_in_primary_store = row[1]
            print "vhd primary storage file:", vhd_file_uuid_in_primary_store
            result_json = get_snapshots(str(volume_id))
            #print result_json
            obj_sss = json.loads(result_json)
            #print obj_sss['listsnapshotsresponse']['count']
            obj_ssss = obj_sss['listsnapshotsresponse']['snapshot']
            for ss in obj_ssss:
                #print ss
                #print ss['volumename'],ss['volumeid'],ss['state'],ss['id']
                cur.execute("SELECT id,path,backup_snap_id FROM snapshots where 1=1 and uuid = '"+ ss['id'] +"' ")
                rows_ss = cur.fetchall()
                for row_s in rows_ss:
                    print row_s
            #send to s3








#root = etree.fromstring(result)
#print etree.tostring(root, pretty_print=True)




