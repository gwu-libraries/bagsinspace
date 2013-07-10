# DSpace Validator 2.0 class file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-12-20

import os
import BagDB
import pybagit.bagit as bagit
import Config as cfg
import Logger
import datetime
import sys

timestamp = str(datetime.datetime.now())
validated_on = timestamp[:19]
timestamp = timestamp[0:10]+'::'+timestamp[11:19]

logPath = cfg.logDirectories['validation']+timestamp+'.log'
log = Logger.Logger(logPath)

numError = 0
invalidBags={}


# Connect to database and select bags with status='new' or bags with status='invalid' and invalid_count<3
try:
    log.addEntry('\nAttempting DB connection.')
    bagdb = BagDB.BagDB(cfg.dbhost, cfg.dbuser, cfg.dbpass, cfg.dbname)
    bags = bagdb.getBagsForValidation()
    #sql = 'select * from bag_record where bag_status="new"'
    #bags = bagdb.getBags(sql)
    bagcount = len(bags)
    log.addEntry('All Bags retrieved. Total bags='+str(bagcount))
except Exception, e:
    log.addEntry("Could not get bags from BagDB. Halting script.\nSystem error message below:\n" + str(e))
    sys.exit()


# Cycle through bags and check for various necessary files before doing hash calculations
for bag in bags:
    invalid = False
    entry = ''
    invalidMsg = ''
    try:
        barcode = bag.getItemBarcode()
        bagtype = bag.getBagType()
        name = bag.getBagName()
        bagpath = bag.getBagPath()
        entry = '\nvalidating bag '+name
        
        # test for bag directory
        if os.path.exists(bagpath):
            entry += '\nbag directory exists: '+bagpath
            
            #test for bag-info.txt
            if os.path.exists(bagpath+'/bag-info.txt'):
                entry += '\nbag-info.txt exists'
            else:
                msg = '\nINVALID! bag-info.txt does NOT exist'
                invalidMsg += msg
                entry += msg
                invalid = True
            #test for bagit.txt
            if os.path.exists(bagpath+'/bagit.txt'):
                entry += '\nbagit.txt exists'
            else:
                msg = '\nINVALID! bagit.txt does NOT exist'
                invalidMsg += msg
                entry += msg
                invalid = True
            #test for manifest-md5.txt
            if os.path.exists(bagpath+'/manifest-md5.txt'):
                entry += 'manifest-md5.txt exists'
            else:
                msg = '\nINVALID! manifest-md5.txt does NOT exist'
                invalidMsg += msg
                entry += msg
                invalid = True
            #test for tagmanifest-md5.txt
            if os.path.exists(bagpath+'/tagmanifest-md5.txt'):
                entry += '\ntagmanifest-md5.txt exists'
            else:
                msg = '\nINVALID! tagmanifest-md5.txt does NOT exist'
                invalidMsg += msg
                entry += msg
                invalid = True
            #test for data directory
            if os.path.exists(bagpath+'/data'):
                entry += '\ndata directory exists'
                #test for METADATA directory
                if os.path.exists(bagpath+'/data/METADATA'):
                    entry += '\nMETADATA directory exists'
                    #test for <barcode>_METS.xml
                    if os.path.exists(bagpath+'/data/METADATA/'+barcode+'_METS.xml'):
                        entry += '\nMETS file exists'
                    else:
                        msg = '\nINVALID! METS file does NOT exist'
                        invalidMsg += msg
                        entry += msg
                        invalid = True
                    if bagtype=='access':
                        #test for <barcode>_MARC.xml
                        if os.path.exists(bagpath+'/data/METADATA/'+barcode+'_MRC.xml'):
                            entry += '\nMARC file exists'
                        else:
                            msg = '\nINVALID! MARC file does NOT exist'
                            invalidMsg += msg
                            entry += msg
                            invalid = True
                    #test for MIX directory
                    if os.path.exists(bagpath+'/data/METADATA/MIX'):
                        entry += '\nMIX directory exists'
                    else:
                        msg = '\nINVALID! MIX directory does NOT exist'
                        invalidMsg += msg
                        entry += msg
                        invalid = True
                else:
                    msg = '\nINVALID! METADATA directory does NOT exist'
                    invalidMsg += msg
                    entry += msg
                    invalid = True
                if bagtype=='access':
                    #test for PDF directory
                    if os.path.exists(bagpath+'/data/PDF'):
                        entry += '\nPDF directory exists'
                        #test for HighRes_<barcode>.pdf
                        if os.path.exists(bagpath+'/data/PDF/HighRes_'+barcode+'.pdf'):
                            entry += '\nHighRes pdf exists'
                        else:
                            entry += '\nINVALID! HighRes pdf does NOT exist'
                            invalidMsg += msg
                            entry += msg
                            invalid = True
                        #test for LowRes_<barcode>.pdf
                        if os.path.exists(bagpath+'/data/PDF/LowRes_'+barcode+'.pdf'):
                            entry += '\nLowRes pdf exists'
                        else:
                            msg = '\nINVALID! LowRes pdf does NOT exist'
                            invalidMsg += msg
                            entry += msg
                            invalid = True
                    else:
                        msg = '\nINVALID! PDF directory does NOT exist'
                        invalidMsg += msg
                        entry += msg
                        invalid = True
                #test for JPEG2K directory
                if os.path.exists(bagpath+'/data/JPEG2K'):
                    entry += '\nJPEG2K directory exists'
                else:
                    msg = '\nINVALID! JPEG2K directory does NOT exist'
                    invalidMsg += msg
                    entry += msg
                    invalid = True
            else:
                msg = '\nINVALID! data directory does NOT exist'
                invalidMsg += msg
                entry += msg
                invalid = True
        else:
            msg = '\nINVALID! bag path does NOT exists: '+bagpath
            invalidMsg += msg
            entry += msg
            invalid = True
    except Exception, e:
        numError += 1
        msg = "\nERROR! System error message below:\n" + str(e)
        invalidMsg += msg
        entry += msg
        invalid = True

    log.addEntry(entry)
    entry = ''
        
    # mark invalid bags as such
    if invalid:
        invalidBags[name]=invalidMsg.lstrip()
        bag.setBagStatus('invalid')
        bag.incrementInvalidCount()
        bagMsg = '['+timestamp+']-'+invalidMsg.lstrip()
        bag.setBagMessage(bagMsg)    
        
    # pass remaining bags on to pybagit to validate hash values
    else:
        try:
            log.addEntry('Passing bag to pybagit for hash validation')
            bagitbag = bagit.BagIt(bagpath)
            errors = bagitbag.validate()
            entry = 'BagIt validation '
            if errors == []:
                bag.setBagStatus('validated')
                bag.setValidatedOn(validated_on)
                entry += 'successful'
            else:
                bag.setBagStatus('invalid')
                entry += 'FAILED!' 
                for err in errors:
                    entry += '\n' + str(err)
                bag.setBagMessage(entry)
                invalidBags[name]=entry
        except Exception, e:
            entry = 'Could not create BagIt object.\n'+str(e)
            bag.setBagStatus('invalid')
            bag.setBagMessage('[' + timestamp + ']-' + entry)
            invalidBags[name]=entry
        log.addEntry(entry)
        
        

entry = '\n\nTotal bags = '+str(bagcount)
entry += '\nInvalid bags: '+str(len(invalidBags))
entry += '\nErrors: '+str(numError)
entry += '\nInvalid bags messages:\n'
for bag in invalidBags:
    entry += '\n'+bag+':\n'+invalidBags[bag]+'\n'
log.addEntry(entry)


#record validation results in database
try:
    bagdb.updateBags(bags)
    log.addEntry('\nBags updated in database')
except Exception, e:
    error = "Could not update bags in BagDB\n" + str(e)
    log.addEntry(error)
    print '\n' + error + '\n'
    sys.exit()
