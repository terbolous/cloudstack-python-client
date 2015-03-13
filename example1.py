#!/usr/bin/python

import CloudStack

api = 'http://172.16.206.143:8080/client/api'
apikey = 'FhlHSpLcOEiB8wVI6xXH8XfA9nLGzdim5eVlUsVa9LXDIleqsAJA1yubYrEHCduSSsCur6gVoEUmQFctHgxv1g'
secret = 'YbftfeOwmC3uBvQfYgSXUwkuUuMeca6G7EKvUZJFeZrivjpFwEMGZlXMqn3rCt0YRy9mPtyt-1F2S9s0IFBqKQ'

cloudstack = CloudStack.Client(api, apikey, secret)

vms = cloudstack.listVirtualMachines()

for vm in vms:
    print "%s %s %s" % (vm['id'], vm['name'], vm['state'])
    print vm
    args = {}
    args["id"] = vm['id']
    cloudstack.createVMSnapshot(  args )
    break

