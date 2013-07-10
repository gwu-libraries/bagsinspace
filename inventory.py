import json
import requests

from settings import INVENTORY_CREDENTIALS as creds


baseurl = '%s:%s/api/%s' % (creds['url'], creds['port'], creds['apiversion'])
auth_header = {'Authorization': 'ApiKey %s:%s' % (creds['user'],
    creds['apikey']), 'Content-Type': 'application/json'}


def _get(model, pk=None, params={}):
    params.update({'format': 'json', 'username': creds['user'],
        'api_key': creds['apikey']})
    if pk:
        url = '%s/%s/%s/' % (baseurl, model, pk)
    else:
        url = '%s/%s/' % (baseurl, model)
    return requests.get(url, params=params, headers=auth_header,
        verify=creds['verify_ssl_cert'])


def _post(model, **data):
    # POST is for new items, not changes. Use PUT or PATCH for changes
    url = '%s/%s/' % (baseurl, model)
    return requests.post(url, data=json.dumps(data), headers=auth_header,
        verify=creds['verify_ssl_cert'])


def _put(model, pk, **data):
    # PUT changes all fields (overwrites with blank if you don't set a value)
    # use PATCH to change one or two fields without setting them all
    url = '%s/%s/%s/' % (baseurl, model, pk)
    return requests.put(url, data=json.dumps(data), headers=auth_header,
        verify=creds['verify_ssl_cert'])


def _patch(model, pk, **data):
    url = '%s/%s/%s/' % (baseurl, model, pk)
    return requests.patch(url, data=json.dumps(data), headers=auth_header,
        verify=creds['verify_ssl_cert'])


def _delete(model, pk):
    url = '%s/%s/%s/' % (baseurl, model, pk)
    return requests.delete(url, headers=auth_header,
        verify=creds['verify_ssl_cert'])


# helper functions

def parse_id(location, uri=False):
    # Parse an object id from the 'location' returned by API 201 response.
    # Option to return just the id or the relative uri,
    # such as: /api/v1/item/38989/c01hf854dw
    uriparts = location.strip('/').split('/')[3:]
    if uri is True:
        return '/%s/' % '/'.join(uriparts)
    else:
        return '/'.join(uriparts[3:])


def bags_to_import(collection_id):
    params = {
        'item__collection__id': collection_id,
        'item__access_loc': ''
        }
    response = _get('bag', params=params)
    print response.status_code
    print response.text
    return response.json()['objects']


