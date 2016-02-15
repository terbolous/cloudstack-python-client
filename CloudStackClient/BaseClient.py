import base64
import hashlib
import hmac
import json
import re
import urllib
import urllib2
from urllib import quote_plus


class BaseClient(object):
    def __init__(self, api, apikey, secret):
        self.api = api
        self.apikey = apikey
        self.secret = secret

    def request(self, command, args):
        args['apikey'] = self.apikey
        args['command'] = command
        args['response'] = 'json'

        params = []

        keys = sorted(args.keys())

        for k in keys:
            params.append(k + '=' + quote_plus(args[k]).replace("+", "%20"))

        query = '&'.join(params)

        signature = base64.b64encode(hmac.new(
            self.secret,
            msg=query.lower(),
            digestmod=hashlib.sha1
        ).digest())

        query += '&signature=' + urllib.quote_plus(signature)

        try:
            response = urllib2.urlopen(self.api + '?' + query)
        except urllib2.HTTPError as error:
            error_msg = ''
            error_data = json.loads(error.read())
            if len(error_data) == 1:
                error_msg = ('ERROR: %s - %s' % (error_data.keys()[0],
                             error_data[error_data.keys()[0]]['errortext']))
            else:
                error_msg = 'ERROR: Received multiple errors.'
            raise RuntimeError(error_msg)

        decoded = json.loads(response.read())

        propertyResponse = command.lower() + 'response'
        if propertyResponse == 'listcountersresponse':
            propertyResponse = 'counterresponse'
        if propertyResponse == 'createconditionresponse':
            propertyResponse = 'conditionresponse'
        if propertyResponse == 'createautoscalepolicyresponse':
            propertyResponse = 'autoscalepolicyresponse'

        if propertyResponse not in decoded:
            if 'errorresponse' in decoded:
                raise RuntimeError(("ERROR: " +
                                    decoded['errorresponse']['errortext']))
            else:
                raise RuntimeError("ERROR: Unable to parse the response")

        response = decoded[propertyResponse]
        result = re.compile(r"^list(\w+)s").match(command.lower())

        if result is not None:
            type = result.group(1)

            if type in response:
                return response[type]
            else:
                # sometimes, the 's' is kept, as in :
                # { "listasyncjobsresponse" : { "asyncjobs" : [ ... ] } }
                type += 's'
                if type in response:
                    return response[type]

        return response
