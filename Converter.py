# DSpace Converter class file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-10-06

import fnmatch
import os
import Item


class Converter:

    # class variables set by config file
    metadataSchema = ''
    metadataPattern = ''
    filePatterns = []   # list of dictionaries with the following fields:
                            # path   (ex = 'IMAGES/')
                            # pattern   (ex = '*.jp2')
                            # bundle (optional)   (ex = 'IMAGES')
                            # description (optional)   (ex = 'A high res photo of a page from the book')
                            # permissions (optional list of dictionaries with following fields:
                                # group   (ex = 'admin')
                                # readORwrite   (ex = 'w')                                
    assetStoreList = []
    register = False
    licenseText = ''

    # general class variables
    bags = []
    items = []
    transformer = ''
    


    def __init__(self, transformer='', assetStoreList=[], register=False, metadataPattern={}, filePatterns=[], metadataSchema='', bags=[], licenseText=''):
        self.transformer = transformer
        self.assetStoreList = assetStoreList
        self.register = register
        self.metadataPattern = metadataPattern
        self.filePatterns = filePatterns
        self.metadataSchema = metadataSchema
        self.bags = bags
        self.licenseText = licenseText
        self.failures = []

    def setMetadataSchema(self, schema):
        self.metadataSchema = schema

    def getMetadataSchema(self):
        return self.metadataSchema

    def setMetadataPattern(self, path, pattern):
        self.metadataPattern = {'path':path, 'pattern':pattern}

    def getMetadataPattern(self):
        return self.metadataPattern
    
    def setFilePatterns(self, patterns):
        self.filePatterns = patterns

    def getFilePatterns(self):
        return self.filePatterns
    
    def addFilePattern(self, path, pattern, bundle, description, permissions):
        self.filePatterns.append({'path':path, 'pattern':pattern, 'bundle':bundle, 'description':description, 'permissions':permissions})
    
    def setAssetStoreList(self, storeList):
        self.assetStoreList = storeList

    def getAssetStoreList(self):
        return self.assetStoreList

    def setRegister(self, boolean):
        self.register = boolean

    def getRegister(self):
        return self.register

    def setTransformer(self, transformer):
        self.transformer = transformer

    def getTransformer(self):
        return self.transformer

    def setLicenseText(self, text):
        self.licenseText = text

    def getTransformer(self):
        return self.transformer

    def getFailures(self):
        return self.failures

    def addBag(self, bag):
        self.bags.append(bag)

    def addBags(self, bags):
        self.bags += bags

    def removeBag(self, name):
        for bag in self.bags:
            if bag.getBagName == name:
                self.bags.remove(bag)
                break

    def clearBags(self):
        self.bags = []

    def convertBags(self):
        for bag in self.bags:
            try:
                print 'converting bag '+bag.getBagName()
                item = Item.Item(name=bag.getItemBarcode())
                #print 'item name='+item.getName()
                item.setPersistentID(bag.getPersistentID())
                #print 'item PID='+item.getPersistentID()
                item.setSchema(self.metadataSchema)
                #print 'item schema='+item.getSchema()
                item.setLicenseText(self.licenseText)
                #print 'item license='+item.getLicenseText()
                item.setTransformer(self.transformer)
                #print 'item transformer set'
                item.setMetadata(self.findMetadata(bag))
                item.setBarcode(bag.getItemBarcode())
                #print 'item metadata found'
                for file in self.findFiles(bag):
                    #print 'adding item file to bitstreams...'
                    item.addBitstream(fileName=file['name'],
                                      registered=self.register,
                                      assetStoreNumber=self.lookupASN(bag),
                                      filePath=file['path'],
                                      bundleName=file['bundle'],
                                      permissions=file['permissions'],
                                      description=file['description'])
                    print 'file added from ASN '+str(self.lookupASN(bag))+': '+file['path']+file['name']
                self.items.append(item)
                print 'Bag '+bag.getBagName()+' successfully converted to item'
            except Exception, e:
                bag.setBagStatus('failed')
                bag.setBagMessage('Could not convert to item. '+str(e))
                self.failures.append(bag)
                print '!!!Bag '+bag.getBagName()+' failed conversion:\n'+str(e)
        return self.items
    

    def findMetadata(self, bag):
        path = bag.getBagPath() + self.metadataPattern['path'].rstrip('/')
        for file in os.listdir(path):
            if fnmatch.fnmatch(file, self.metadataPattern['pattern']):
                return path + '/' + file
            

    def findFiles(self, bag):
        output = []
        for pattern in self.filePatterns:
            path = bag.getBagPath() + pattern['path'].rstrip('/')
            for file in os.listdir(path):
                if fnmatch.fnmatch(file, pattern['pattern']):
                    bitstreampath = bag.getItemBarcode() + '/' + bag.getBagName() + '/' + pattern['path'].strip('/')
                    output.append({'path':bitstreampath, 'name':file, 'bundle':pattern['bundle'], 'description':pattern['description'], 'permissions':pattern['permissions']})
        return output


    def lookupASN(self, bag):
        assetStorePath = bag.getAttribute('asset_store_path').rstrip('/')+'/'
        for asn in self.assetStoreList:
            if asn == assetStorePath:
                return self.assetStoreList.index(asn)

    
