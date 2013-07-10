# DSpace SimpleArchive class file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-09-24

import libxml2
import libxslt


class Transformer:

    currentFormat = ''

    stylesheets = {'MARC':'', 'MODS':'', 'EAD':''}

    qdcDoc = ''
    qdcStyle = ''

    dspaceDoc = ''
    dspaceStyle = ''

    assumption = ''


    # get stylesheet defaults from config
    # self.setMARCtoQDCStylesheet(marc2qdcFile)
    # self.setQDCtoDSpaceDCStylesheet(qdc2dsdcFile)


    def __init__(self, qdc2dspace, marc2qdc='', mods2qdc='', ead2qdc='', default='MARC', assumption=''):
        
        self.stylesheets['MARC'] = marc2qdc
        self.stylesheets['MODS'] = mods2qdc
        self.stylesheets['EAD'] = ead2qdc
        self.assumption = assumption

        self.setQDCtoDSpaceStylesheet(qdc2dspace)

        self.setDefaultMetadataFormat(default)
        

    def updateStylesheets(self, qdc2dspace='', marc2qdc='', mods2qdc='', ead2qdc=''):
        if marc2qdc != '':
            self.stylesheets['MARC'] = marc2qdc
        if mods2qdc != '':
            self.stylesheets['MODS'] = mods2qdc
        if ead2qdc != '':
            self.stylesheets['EAD'] = ead2qdc
        if qdc2dspace != '':
            self.setQDCtoDSpaceStylesheet(qdc2dspace)

    def setDefaultMetadataFormat(self, default):
        self.currentFormat = default
        self.setSourceMDtoQDCStylesheet(self.stylesheets[default])    
    
    def setSourceMDtoQDCStylesheet(self, filepath):
        self.qdcDoc = libxml2.parseFile(filepath)
        self.qdcStyle = libxslt.parseStylesheetDoc(self.qdcDoc)

    def setQDCtoDSpaceStylesheet(self, filepath):
        self.dspaceDoc = libxml2.parseFile(filepath)
        self.dspaceStyle = libxslt.parseStylesheetDoc(self.dspaceDoc)

    def setAssumption(self, assumption):
        self.assumption = assumption

    def createDSpaceDCfromMetadata(self, mdFormat, sourceFile, targetFile, barcode=''):
        barcode = '"' + barcode + '"'
        if mdFormat == 'DC' or mdFormat == 'QDC' :
            sourceMD = ''
            qdc = libxml2.parseFile(sourceFile)
        else:
            if mdFormat != self.currentFormat:
                self.currentFormat = mdFormat
                self.setSourceMDtoQDCStylesheet(self.stylesheets[mdFormat])
            sourceMD = libxml2.parseFile(sourceFile)
            params = None
            if self.assumption != '':
                params = {"assumption":self.assumption, "barcode":barcode}
            qdc = self.qdcStyle.applyStylesheet(sourceMD, params)
        dsdc = self.dspaceStyle.applyStylesheet(qdc, None)
        self.dspaceStyle.saveResultToFilename(targetFile, dsdc, 0)
        if sourceMD:
            sourceMD.freeDoc()
        qdc.freeDoc()
        dsdc.freeDoc()
