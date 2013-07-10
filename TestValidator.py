# Test Bag Validator script file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-10-12

import sys
import pybagit.bagit as bagit
import BagDB
import Config as cfg
import Logger

logPath = cfg.logs['validation']
log = Logger.Logger(logPath)
barcodeList = [32882019064834,32882019065070,32882019067720,32882019067738,32882018661341]

# Connect to database and select bags with status='new' or 'failed'
# (retry failed bags in case they had not finished uploading to  the server on previous attempt)
try:
    print '\nAttempting DB connection.'
    bagdb = BagDB.BagDB(cfg.dbhost, cfg.dbuser, cfg.dbpass, cfg.dbname)
    bags = bagdb.getBagsByBarcode(barcodeList)
    print '\nNew Bags retrieved. Total bags='+str(len(bags))
except Exception, e:
    error = "Could not get bags from BagDB. Halting script.\nSystem error message below:\n" + str(e)
    print '\n' + error + '\n'
    log.addEntry(error)
    sys.exit()
    
#for every bag, run validation script and update status accordingly
for record in bags:
    print '\nEntering for loop.'
    try:
        print '\ngetting path'
        path = record.getBagPath()
        print '\npath='+path
        print '\ncreating bagit object'
        bag = bagit.BagIt(path)
        print '\nvalidating'
        errors = bag.validate()
        print '\nbag errors='+str(errors)
        msg = ''
        if errors == []:
            print '\nno errors, setting status to validate'
            record.setBagStatus('validated')
            print '\ncreating msg'
            msg = 'Bag ' + record.getItemBarcode() + ' successfully validated'
            print '\nmsg='+msg
        else:
            print 'nvalidation failed. setting status=failed'
            record.setBagStatus('failed')
            msg = 'Bag ' + record.getItemBarcode() + ' failed validation' 
            for err in errors:
                msg += '\n' + str(err)
            print 'error msg ='+msg
            record.setBagMessage(msg)
    except Exception, e:
        print '\nexception caught'
        record.setBagStatus('failed')
        msg = 'Could not create BagIt object.'
        record.setBagMessage(msg)
        msg += ' Process failed. Skipping object.\n' + str(e)
    print '\n' + msg + '\n'
    log.addEntry(msg)

#record validation results in database
try:
    bagdb.updateBags(bags)
except Exception, e:
    error = "Could not update bags in BagDB\n" + str(e)
    print '\n' + error + '\n'
    log.addEntry(error)
    sys.exit()
