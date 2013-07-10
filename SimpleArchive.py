# DSpace SimpleArchive class file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-09-08


import os
import datetime


class SimpleArchive:
    
    def __init__(self, path, name='', items=[]):
        self.path = path
        self.name = name
        self.batchDir = ''
        self.generateBatchDir()
        
        self.items = []
        for item in items:
            self.addItem(item)
    
    
    def getBatchDir(self):
        return self.batchDir
    
    def setBatchDir(self, batchDir):
        self.batchDir = batchDir

    def generateBatchDir(self):
        if self.name == '':
            dt = datetime.datetime.now()
            self.name = "importbatch-" + str(dt.date()) + "-" + str(dt.time())
        self.batchDir = self.path.rstrip('/') + '/' + self.name
    
    
    def addItems(self, items):
        for item in items:
            self.addItem(item)    
    
    def addItem(self, item):
        item.setBatchDir(self.batchDir)
        self.items.append(item)

    def removeItem(self, name):
        for item in self.items:
            if item.getName() == name:
                self.items.remove(item)
                break

    def removeItems(self, names):
        for name in names:
            self.removeItem(name)

    def setPath(self, path):
        self.path = path
        self.generateBatchDir()

    def getPath(self):
        return self.path

    def setName(self, name):
        self.name = name
        self.generateBatchDir()

    def getName(self):
        return self.name
        
    
    
    def buildSimpleArchive(self):
        try:
            print 'making Batch Directory'
            os.mkdir(self.batchDir)
            print 'Batch directory created: '+self.batchDir
            for item in self.items:
                print 'building directory for item '+item.getName()
                item.buildItemDirectory()
                print item.getName()+' directory built successfully'
        except Exception, err:
            error_message = 'Error creating batch directory.\nError Message: ' + str(err) + '\n'
            print error_message
            raise Exception, error_message

    
    


