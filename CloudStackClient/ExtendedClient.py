from Client import Client


class ExtendedClient(Client):
    '''
    This is designed to work with the CloudStack API extension which can be
    found at https://github.com/jasonhancock/cloudstack-api-extension
    '''

    def getUserData(self, args={}):
        if 'id' not in args:
            raise RuntimeError("Missing required argument 'id'")

        return self.request('getUserData', args)

    def listBundles(self, args={}):
        return self.request('listBundles', args)

    def deployBundle(self, args={}):
        if 'bundle' not in args:
            raise RuntimeError("Missing required argument 'bundle'")

        return self.request('bundle', args)

    def listVPCs(self, args={}):
        return self.request('listVPCs', args)

    def createVPC(self, args={}):
        if 'cidr' not in args:
            raise RuntimeError("Missing required argument 'cidr'")
        if 'displaytext' not in args:
            raise RuntimeError("Missing required argument 'displaytext'")
        if 'name' not in args:
            raise RuntimeError("Missing required argument 'name'")
        if 'vpcofferingid' not in args:
            raise RuntimeError("Missing required argument 'vpcofferingid'")
        if 'zoneid' not in args:
            raise RuntimeError("Missing required argument 'zoneid'")
        return self.request('createVPC', args)

    def deleteVPC(self, args={}):
        if 'id' not in args:
            raise RuntimeError("Missing required argument 'id'")
        return self.request('deleteVPC', args)
