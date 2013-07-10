# DSpace Item class file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-09-08

import os

class Item:


    def __init__(self, name, batchDir='', subDir='', licenseText='', persistentID='', schema='', metadata='', transformer='', bitstreams=[], barcode=''):
        self.name = name
        self.batchDir = batchDir.rstrip('/')
        self.subDir = subDir.rstrip('/')
        self.licenseText = licenseText
        self.persistentID = persistentID
        self.schema = schema
        self.metadata = metadata
        self.transformer = transformer
        self.barcode = barcode
        self.bitstreams = bitstreams    #each bitstream item in this list is a dictionary of the following fields:
                                            #registered(boolean),
                                            #assetStoreNumber(string),
                                            #filePath(string),
                                            #fileName(string),
                                            #bundleName(string),
                                            #description(string),
                                            #permission(list) --> The permissions list contains tuples of group names and a flag for read or write permission
                                            #e.g.  permissions=[('admin','w'),('students','r')...]

    def buildItemDirectory(self):
        print 'building subdir'
        self.makeSubDir()
        print 'making contents file'
        self.makeContentsFile()
        print 'making handle file'
        self.makeHandleFile()
        print 'making dublin core file'
        self.makeDublinCoreFile()
        print 'making license file'
        self.makeLicenseFile()


    def makeSubDir(self):
        if self.subDir == '':
            self.subDir = self.name
        os.mkdir(self.batchDir + '/' + self.subDir)


    def makeContentsFile(self):
        filename = self.batchDir + '/' + self.subDir + '/contents'
        contentsFile = open(filename, 'w')
        for bitstream in self.bitstreams:
            line = ''
            if bitstream['registered']:
                line += '-r -s ' + bitstream['assetStoreNumber'] + ' -f ' + bitstream['filePath'] + '/'
            line += bitstream['fileName']
            if bitstream['bundleName'] != '':
                line += '\tbundle:' + bitstream['bundleName']
            if bitstream['permissions'] != []:
                line += '\tpermissions:'
                for permission in bitstream['permissions']:
                    line += ' -' + permission[1] + " '" + permission[0] + "'"
            if bitstream['description'] != '':
                line += '\tdescription: ' + bitstream['description']
            contentsFile.write(line + '\n')
        if self.licenseText != '':
            contentsFile.write('license.txt')
        contentsFile.close()
        

    def makeHandleFile(self):
        filename = self.batchDir + '/' + self.subDir + '/handle'
        handleFile = open(filename,'w')
        handleFile.write(self.persistentID)
        handleFile.close()


    def makeDublinCoreFile(self):
        target = self.batchDir + '/' + self.subDir + '/dublin_core.xml'
        print 'target DublinCore file ='+target
        self.transformer.createDSpaceDCfromMetadata(self.schema, self.metadata, target, self.barcode)
            
    
    def makeLicenseFile(self):
        if self.licenseText != '':
            filename = self.batchDir + '/' + self.subDir + '/license.txt'
            licenseFile = open(filename, 'w')
            licenseFile.write(self.licenseText)
            licenseFile.close()
    
    
    def setBatchDir(self, path):
        self.batchDir = path.rstrip('/')
    
    def getBatchDir(self):
        return self.batchDir
    
    
    def setSubDir(self, name):
        self.subDir = name.rstrip('/')
    
    def getSubDir(self):
        return self.subDir
    
    
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    
    def setPersistentID(self, pid):
        self.persistentID = pid
    
    def getPersistentID(self):
        return self.persistentID


    def setSchema(self, schema):
        self.schema = schema
    
    def getSchema(self):
        return self.schema
    
    
    def setLicenseText(self, text):
        self.licenseText = text
    
    def getLicenseText(self):
        return self.licenseText

    def setTransformer(self, transformer):
        self.transformer = transformer
    
    def getTransformer(self):
        return self.transformer

    def setBarcode(self, x):
        self.barcode = x

    def getBarcode(self):
        return self.barcode


    def addBitstream(self, fileName, registered=False, assetStoreNumber='1',
                     filePath='', bundleName='', permissions=[], description=''):
        bitstream = {}
        bitstream['fileName']=fileName
        bitstream['registered']=registered
        bitstream['assetStoreNumber']=str(assetStoreNumber)
        bitstream['filePath']=filePath
        bitstream['bundleName']=bundleName
        bitstream['description']=description
        bitstream['permissions']=permissions        #permissions should be a list of tuples stating a group name and read or write permission
                                                    #e.g. permissions=[('admin','w'),('students','r'),('colldev','r')]
        if self.bitstreams:
            self.bitstreams.append(bitstream)
        else:
            self.bitstreams=[bitstream]
        
    def removeBitstream(self, fileName):
        for bitstream in self.bitstreams:
            if bitstream['fileName']==fileName:
                self.bitstreams.remove(bitstream)
                break
    
    def editBitstream(self, fileName, attribute, value):
        for bitstream in self.bitstreams:
            if bitstream['fileName'] == fileName:
                bitstream[attribute] = value
                break

    def setMetadata(self, mdFile):
        self.metadata = mdFile

    def getMetadata(self):
        return self.metadata
    
    
    



















            
            
        
