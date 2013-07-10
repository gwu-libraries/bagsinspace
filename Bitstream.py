# DSpace Bitstream class file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-10-06

class Bitstream:

    fileName = ''
    filePath = ''           #exclude file name and final slash
    assetStoreNumber = ''   #as represented in the dspace config file
    registered = ''         #boolean           
    bundleName = ''         #optional
    description = ''        #optional
    permissions = []        #optional, list of tuples (group, permission)
                            #e.g. [('admin','w'),('students','r')]

    def __init__(self, name, path, asset=0, registered=False, bundle='', description='',permissions=[]):
        self.fileName = name
        self.filePath = path.rstrip('/')
        self.assetStoreNumber = asset
        self.registered = registered
        self.bundleName = bundle
        self.description = description
        self.permissions = permissions


    def setRegistered(self, registered):
        self.registered = registered

    def getRegistered(self):
        return self.registered

    def setAssetStoreNumber(self, num):
        self.assetStoreNumber = num

    def getAssetStoreNumber(self):
        return self.assetStoreNumber

    def setFilePath(self, path):
        self.filePath = path

    def geFilePath(self):
        return self.filePath.rstrip('/')

    def setFileName(self, name):
        self.fileName = name

    def geFileName(self):
        return self.fileName

    def setBundleName(self, name):
        self.bundleName = name

    def geBundleName(self):
        return self.bundleName

    def setDescription(self, desc):
        self.description = desc

    def geDescription(self):
        return self.description

    def addPermission(self, group, permission):
        self.permissions.append((group,permission))

    def removePermission(self, group):
        for permission in self.permissions:
            if permission[0]==group:
                self.permissions.remove(permission)

    def getPermissions(self):
        return self.permissions
