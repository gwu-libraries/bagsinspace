# Noid class file
#
# For use with Noid permanent identifier creation system (see: http://search.cpan.org/dist/Noid/noid)
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-09-01

from urllib import urlopen
import json

class Noid:

    #noidURL = 'http://gwnma.wrlc.org/nd/noidu_t1'           #TODO: change this to production URL

    def __init__(self, url):
        self.noidURL = url


    def setURL(self, altURL):
        self.noidURL = altURL


    def mint(self, quantity=1):
        # TODO: add test for int value, throw error if not
        #mintURL = self.noidURL + '?mint+' + str(quantity)        #build url
        mintURL = '%s/mint/ark/%s' % (self.noidURL, quantity)
        output = urlopen(mintURL).read()                    #make the url call to noidu
        output = json.loads(output)
        if quantity == 1:                                   #if single mint, return result pid (with "id: " removed)
            return output[0]['identifier']
        return [item['identifier'] for item in output]      #else, return pids as a list (with "id: " removed)


    def bind(self, itemPID, itemURL, verbose=False):
        #bindURL = self.noidURL + '?bind+set+' + itemPID + '+item+' + itemURL     #build the url
        bindURL = '%s/bind/%s?object_url=%s&object_type=i' % (self.noidURL, itemPID, itemURL)
        output = urlopen(bindURL).read().rstrip()                           #make the call to noid and remove trailing newlines from response
        if output[0:5] == 'error':                                          #if error message return False
            if not verbose:                                                        #if verbose return False + msg
                return False
            return (False, output)
        if not verbose:                                                        #else return True
            return True
        output = output.split('\n')                                             #if verbose return True + dictionary of elements
        dictionary = {}
        for line in output:
            key, value = line.split(':')
            dictionary[key] = value.strip()
        return (True, dictionary)                                           
