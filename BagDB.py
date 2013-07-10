# BagDB class file
#
# For use with MySQL database
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-09-01

import MySQLdb
import Bag

class BagDB:
    
    def __init__(self, host, username, password, dbname):
        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname
        
        self.db = MySQLdb.connect(host, username, password, dbname)
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        
    def shutdown(self):
        self.db.commit()
        self.db.close()

    def commit(self):
        self.db.commit()
    
    
#    def rawDump(self):
#        sql = 'SELECT * FROM bag_record'
#        self.cursor.execute(sql)
#        return self.cursor.fetchall()
    
    
    def getBagsForImport(self):
        sql = 'SELECT * FROM bag_record WHERE ((bag_status = "validated" or bag_status = "updated") AND bag_type = "access")'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return self.makeBags(results)

    def getBagsForExport(self):
        sql = 'SELECT * FROM bag_record WHERE (bag_status = "imported" AND bag_type = "access")'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return self.makeBags(results)

    def getBagsForValidation(self):
        #sql = 'SELECT * FROM bag_record WHERE (bag_status = "new" or (bag_status = "invalid" and invalid_count<3))'
        sql = 'SELECT * FROM bag_record WHERE (bag_status = "new" OR bag_status = "invalid") AND project_name!="IBT-microfilm"'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return self.makeBags(results)
    
    
    def getAllBags(self):
        sql = 'SELECT * FROM bag_record'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return self.makeBags(results)
    
    
    def getNewBags(self):
        sql = 'SELECT * FROM bag_record WHERE bag_status = "new"'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return self.makeBags(results)
    
    
    def getFailedBags(self):
        sql = 'SELECT * FROM bag_record WHERE bag_status = "failed"'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return self.makeBags(results)
    
    
#    def getBagsByStatus(self, status):
#        sql = 'SELECT * FROM bag_record WHERE bag_status = "' + status + '"'
#        self.cursor.execute(sql)
#        results = self.cursor.fetchall()
#        return results
    
    
    def getBagsByStatus(self, statusList):
        sql = 'SELECT * FROM bag_record WHERE (bag_status = "' + statusList[0] + '"'
        for status in statusList[1:]:
            sql += ' or bag_status = "' + status + '"'
        sql += ')'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return self.makeBags(results)
    
    
    def getBags(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return self.makeBags(results)

    def getBagsByBarcode(self, barcodeList):
        sql = 'SELECT * FROM bag_record WHERE (item_barcode="' + str(barcodeList[0]) + '"'
        for barcode in barcodeList[1:]:
            sql += ' or item_barcode="' + str(barcode) + '"'
        sql += ')'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return self.makeBags(results)
    
    def updateBags(self, bagList):
        output = {}
        for bag in bagList:
            attributes = bag.getUpdatedAttributes()
            if attributes == []: continue
            else:
                sql = 'UPDATE bag_record SET ' + attributes[0] + ' = "' + bag.getAttribute(attributes[0]) + '"'
                for attribute in attributes[1:]:
                    if (attribute=='invalid_count' or attribute=='exported' or attribute=='source_deleted'):
                        sql += ', ' + attribute + ' = ' + str(bag.getAttribute(attribute))
                    else:
                        if attribute=='bag_message':
                            value = self.db.escape_string(bag.getAttribute(attribute))                        
                        else:
                            value = bag.getAttribute(attribute)
                        sql += ', ' + attribute + ' = "' + value + '"'
                sql += ' WHERE record_id = ' + str(bag.getRecordID())
                try:
                    self.cursor.execute(sql)
                    results = self.cursor.fetchall()
                    output[bag.getBagName()] = True
                except Exception, e:
                    output[bag.getBagName()] = False
                    print e
        return output
    
    
    def insertBags(self, bagList):
        output = {}
        for bag in bagList:
            attributes = bag.getInsertableAttributes()
            sql = 'INSERT INTO bag_record SET ' + attributes[0] + ' = "' + bag.getAttribute(attributes[0]) + '"'
            for attribute in attributes[1:]:
                sql += ', ' + attribute + ' = "' + bag.getAttribute(attribute) + '"'
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                output[bag.getBagName()] = True
            except Exception, e:
                output[bag.getBagName()] = False
                print e
        return output
    
    def makeBags(self, records):
        
        bags = []
        for record in records:
            bag = Bag.Bag(recordID = record['record_id'],
                      itemBarcode = record['item_barcode'],
                      assetStorePath = record['asset_store_path'],
                      projectName = record['project_name'],
                      bagName = record['bag_name'],
                      bagStatus = record['bag_status'],
                      bagMessage = record['bag_message'],
                      persistentID = record['persistent_id'],
                      timeStamp = record['time_stamp'],
                      bagType = record['bag_type'],
                      sourceDeleted = record['source_deleted'],
                      invalid_count = record['invalid_count'],
                      exported = record['exported'],
		      created_on = record['created_on'],
		      validated_on = record['validated_on'],
		      imported_on = record['imported_on'],
		      dspace_collection_number = record['dspace_collection_number'],
		      bag_location = record['bag_location']
                      )
            bags.append(bag)
        return bags
