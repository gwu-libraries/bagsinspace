# DSpace BagCrawler class file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-10-05

import os
import fnmatch

class BagCrawler:

    currentBag = '' # a bag object for crawling through
    metadataPattern = {}   # dictionary of (path, matchpattern) for primary metadata file e.g. ('METADATA/','[1-9]_MRC.xml')
    filePatterns = []   # list of dictionaries with the following fields:
                            # path   (ex = 'IMAGES/')
                            # pattern   (ex = '*.jp2')
                            # bundle (optional)   (ex = 'IMAGES')
                            # description (optional)   (ex = 'A high res photo of a page from the book')
                            # permissions (optional list of dictionaries with following fields:
                                # group   (ex = 'admin')
                                # readORwrite   (ex = 'w')


    def __init__(self, metadataPattern=('',''), filePatterns=[], firstBag=''):
        self.metadataPattern = metadataPattern
        self.fileMatches = filePatterns
        self.currentBag = firstBag 

    def loadBag(self, bag):
        self.currentBag = bag

    def setMetadataPattern(self, patternDict):
        self.metadataPattern = patternDict

    def getMetadataPattern(self):
        return self.metadataPattern

    def setFilePatterns(self, patternList):
        self.filePattern = patternList

    def addFilePattern(self, patternDict):
        self.filePatterns.append(patternDict)

    def getFilePatterns(self):
        return self.filePatterns

    

    def getBagItText(self):
        path = bag.getBagPath() + '/bagit.txt'
        bagit = open(path)
        return bagit.read()

    def getManifestText(self):
        path = bag.getBagPath() + '/manifest-md5.txt'
        manifest = open(path)
        return manifest.read()

    def getBagInfoText(self):
        path = bag.getBagPath() + '/bag-info.txt'
        baginfo = open(path)
        return baginfo.read()

    def findMetadata(self):
        path = self.currentBag.getBagPath() + '/data/' + self.metadataPattern['path'].rstrip('/')
        for file in os.listdir(path):
            if fnmatch.fnmatch(file, self.metadataPattern['pattern']):
                return path + '/' + file

    def findFiles(self):
        output = []
        for pattern in self.filePatterns:
            path = self.currentBag.getBagPath() + '/data/' + pattern['path'].rstrip('/')
            for file in os.listdir(path):
                if fnmatch.fnmatch(file, pattern['pattern']):
                    output.append({'path':path, 'name':file, 'bundle':pattern['bundle'], 'description':pattern['description'], 'permissions':pattern['permissions']})
        return output
