from urllib import urlopen, urlencode
import json

class IDService:

    def __init__(self, url):
        self.url = url

    def setURL(self, url):
        self.url = url

    def mint(self, minter_name, quantity=1):
        mint_url = '%s/mint/%s/%s' % (self.url, minter_name, quantity)
        response = urlopen(mint_url)
        if response.code == 200:
           ids = json.loads(response.read())
           if quantity == 1:
               return ids[0]['identifier']
           return [id_dict['identifier'] for id_dict in ids]
               
    def bind(self, identifier, object_type='i', object_url='', description='', verbose=False):
        bind_url = '%s/bind/%s' % (self.url, identifier)
        params = urlencode({'object_type':object_type, 'object_url':object_url, 'description':description})
        response = urlopen(bind_url, params)
        if response.code == 200:
            if not verbose:
                return True
            id_dict = json.loads(response.read())[0]
            return (True, id_dict)
        elif not verbose:
            return False
        return (False, str(response.code))
            
            
            
