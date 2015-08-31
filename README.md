CloudStack Python Client
========================

Python client library for the CloudStack User API. For older versions,
see the [tags](https://github.com/terbolous/cloudstack-python-client/tags).


from https://github.com/terbolous/cloudstack-python-client


Examples
--------

List all virtual machines

```python
#!/usr/bin/python

import CloudStack

api = 'http://example.com:8080/client/api'
apikey = 'API KEY'
secret = 'API SECRET'

cloudstack = CloudStack.Client(api, apikey, secret)

vms = cloudstack.listVirtualMachines()

for vm in vms:
    print "%s %s %s" % (vm['id'], vm['name'], vm['state'])
```


   
Asynchronous tasks

```python
#!/usr/bin/python

import CloudStack

api = 'http://example.com:8080/client/api'
apikey = 'API KEY'
secret = 'API SECRET'

cloudstack = CloudStack.Client(api, apikey, secret)

job = cloudstack.deployVirtualMachine({
    'serviceofferingid': '2',
    'templateid':        '214',
    'zoneid':            '2'
})

print "VM being deployed. Job id = %s" % job['jobid']

print "All Jobs:"
jobs = cloudstack.listAsyncJobs({})
for job in jobs:
    print  "%s : %s, status = %s" % (job['jobid'], job['cmd'], job['jobstatus'])

```

TODO:
-----
There is a lot to do to clean up the code and make it worthy of production. This
was just a rough first pass.
