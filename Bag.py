# Bag class file
#
# For use with Noid permanent identifier creation system (see: http://search.cpan.org/dist/Noid/noid)
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-09-02

import os

class Bag:
        
    def __init__(self, recordID='', itemBarcode='', assetStorePath='',
                 projectName='', bagName='', bagStatus='',
                 bagMessage='', persistentID='', timeStamp='',
                 bagType='',sourceDeleted=0, exported=0, invalid_count=0,
                 validated_on='', imported_on='', created_on='',
                 bag_location='', dspace_collection_number=''):
    
        self.attributes = {}
        self.attributes['record_id'] = recordID
        self.attributes['item_barcode'] = itemBarcode
        self.attributes['asset_store_path'] = assetStorePath
        self.attributes['project_name'] = projectName
        self.attributes['bag_name'] = bagName
        self.attributes['bag_status'] = bagStatus
        self.attributes['bag_message'] = bagMessage
        self.attributes['persistent_id'] = persistentID
        self.attributes['time_stamp'] = timeStamp
        self.attributes['bag_type'] = bagType
        self.attributes['source_deleted'] = sourceDeleted
        self.attributes['exported']=exported
        self.attributes['invalid_count']=invalid_count
        self.attributes['validated_on']=validated_on
        self.attributes['imported_on']=imported_on
        self.attributes['created_on']=created_on
        self.attributes['bag_location']=bag_location
        self.attributes['dspace_collection_number']=dspace_collection_number

        # clean up bad input if necessary
        # (empty strings work better than None elements)
        for att in self.attributes:
            if self.attributes[att]==None:
                self.attributes[att]=''
    
        self.updatedAttributes = []
    
    
### Getter / Setter Methods ###

    def getBagPath(self):
	if self.attributes['bag_location']:
            return os.path.join(self.attributes['bag_location'], self.attributes['bag_name'])
        path = self.attributes['asset_store_path'].rstrip('/')
        path += '/' + self.attributes['item_barcode']
        path += '/' + self.attributes['bag_name']
        return path
    
    def getAttribute(self, x):
        return self.attributes[x]
    
    def setAttribute(self, att, val):
        self.attributes[att] = val
        self.updatedAttributes.append(att)
    
    def getUpdatedAttributes(self):
        return self.updatedAttributes

    def getInsertableAttributes(self):
        returnAtts = [att for att in self.attributes if (att != 'record_id' and att != 'time_stamp' and self.attributes[att] != None and self.attributes[att] != '')]
        return returnAtts
    
    
#    def setRecordID(self, x):
#        self.recordID = x
    
    def getRecordID(self):
        return self.attributes['record_id']
    
    
    def setItemBarcode(self, x):
        self.attributes['item_barcode'] = x
        self.updatedAttributes.append('item_barcode')
    
    def getItemBarcode(self):
        return self.attributes['item_barcode']
    
    
    def setAssetStorePath(self, x):
        self.attributes['asset_store_path'] = x
        self.updatedAttributes.append('asset_store_path')
    
    def getAssetStorePath(self):
        return self.attributes['asset_store_path']
    
    
    def setProjectName(self, x):
        self.attributes['project_name'] = x
        self.updatedAttributes.append('asset_store_path')
    
    def getProjectName(self):
        return self.attributes['project_name']
    
    
    def setBagName(self, x):
        self.attributes['bag_name'] = x
        self.updatedAttributes.append('bag_name')
    
    def getBagName(self):
        return self.attributes['bag_name']
    
    
    def setBagStatus(self, x):
        self.attributes['bag_status'] = x
        self.updatedAttributes.append('bag_status')
    
    def getBagStatus(self):
        return self.attributes['bag_status']
    
    
    def setBagMessage(self, x):
        if self.attributes['bag_message'] != '':
		x = '\n' + x
	self.attributes['bag_message'] += x
        self.updatedAttributes.append('bag_message')
    
    def getBagMessage(self):
        return self.attributes['bag_message']
    
    
    def setPersistentID(self, x):
        self.attributes['persistent_id'] = x
        self.updatedAttributes.append('persistent_id')
    
    def getPersistentID(self):
        return self.attributes['persistent_id']

    def setBagType(self, x):
        self.attributes['bag_type'] = x
        self.updatedAttributes.append('bag_type')
    
    def getBagType(self):
        return self.attributes['bag_type']

    def setSourceDeleted(self, x):
        self.attributes['source_deleted'] = x
        self.updatedAttributes.append('source_deleted')
    
    def getSourceDeleted(self):
        return self.attributes['source_deleted']

    def getExported(self):
        return self.attributes['exported']

    def setExported(self, x):
        self.attributes['exported'] = x
        self.updatedAttributes.append('exported')

    def getInvalidCount(self):
        return self.attributes['invalid_count']

    def setInvalidCount(self, x):
        self.attributes['invalid_count'] = x
        self.updatedAttributes.append('invalid_count')

    def incrementInvalidCount(self):
        x = self.attributes['invalid_count']
        self.setInvalidCount(x+1)
    
    
#    def setTimeStamp(self, x):
#        self.attributes['time_stamp'] = x
#        self.updatedAttributes.append('time_stamp')
    
    def getTimeStamp(self):
        return self.attributes['time_stamp']

    def setValidatedOn(self, x):
        self.attributes['validated_on'] = x
        self.updatedAttributes.append('validated_on')
    
    def getValidatedOn(self):
        return self.attributes['validated_on']
    

    def setImportedOn(self, x):
        self.attributes['imported_on'] = x
        self.updatedAttributes.append('imported_on')
    
    def getImportedOn(self):
        return self.attributes['imported_on']


    def setCreatedOn(self, x):
        self.attributes['created_on'] = x
        self.updatedAttributes.append('created_on')
    
    def getCreatedOn(self):
        return self.attributes['created_on']


    def setBagLocation(self, x):
        self.attributes['bag_location']=x
        self.updatedAttributes.append('bag_location')

    def getBagLocation(self):
        return self.attributes['bag_location']


    def setDspaceCollectionNumber(self, x):
        self.attributes['dspace_collection_number']=x
        self.updatedAttributes.append('dspace_collection_number')

    def getDspaceCollectionNumber(self):
        return self.attributes['dspace_collection_number']
