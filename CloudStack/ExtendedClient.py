from Client import Client

class ExtendedClient(Client):
    '''
    This is designed to work with the CloudStack API extension which can be
    found at https://github.com/jasonhancock/cloudstack-api-extension 
    '''

    def getUserData(self, args={}):
        if not 'id' in args:
            raise RuntimeError("Missing required argument 'id'")

        return self.request('getUserData', args) 

    def listBundles(self, args={}):
        return self.request('listBundles', args) 
    
    def deployBundle(self, args={}):
        if not 'bundle' in args:
            raise RuntimeError("Missing required argument 'bundle'")

        return self.request('bundle', args) 

    def listVPCs(self, args={}):
        return self.request('listVPCs', args)

    def createVPC(self, args={}):
        if not 'cidr' in args:
            raise RuntimeError("Missing required argument 'cidr'")
        if not 'displaytext' in args:
            raise RuntimeError("Missing required argument 'displaytext'")
        if not 'name' in args:
            raise RuntimeError("Missing required argument 'name'")
        if not 'vpcofferingid' in args:
            raise RuntimeError("Missing required argument 'vpcofferingid'")
        if not 'zoneid' in args:
            raise RuntimeError("Missing required argument 'zoneid'")
        return self.request('createVPC', args)


    def deleteVPC(self, args={}):
        if not 'id' in args:
            raise RuntimeError("Missing required argument 'id'")
        return self.request('deleteVPC', args)


