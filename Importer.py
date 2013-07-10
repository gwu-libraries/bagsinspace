# DSpace Importer class file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-10-12

import subprocess as sub
import sys
import BagDB
import Bag
import Noid
import Converter
import Transformer
import Item
import SimpleArchive
import Logger
import Config as cfg
import datetime

timestamp = str(datetime.datetime.now())
imported_on = timestamp[:19]
timestamp = timestamp[0:10]+'::'+timestamp[11:19]

logPath = cfg.logDirectories['import']+timestamp+'.log'
log = Logger.Logger(logPath)

# Get valid bags from database
try:
    bagdb = BagDB.BagDB(cfg.dbhost, cfg.dbuser, cfg.dbpass, cfg.dbname) #
    #bags = bagdb.getBagsForImport()
    sql = 'SELECT * FROM bag_record WHERE dspace_collection_number=14 AND bag_status="validated" AND bag_type="access" AND project_name LIKE "G%"'
    bags = bagdb.getBags(sql)
    bagcount = len(bags)
    msg = 'Bags retrieved. Total bags='+str(bagcount)
    log.addEntry(msg)
except Exception, e:
    error = "Could not get bags from BagDB. Halting script.\nSystem error message below:\n" + str(e)
    log.addEntry(error)
    sys.exit()

# Set up the NOID object
try:
    log.addEntry('Setting up NOID...')
    noid = Noid.Noid(cfg.noidurl)
    log.addEntry('success')
except Exception, e:
    error = 'Error setting up NOID. Halting script.\nSystem error message below:\n' + str(e)
    log.addEntry(error)
    sys.exit()
    
# Mint new PIDs (persistent identifiers) for each bag
# Predict dspace url for each bag and bind it to the PID
# Update the database with the bags' new PIDs
try:
    msg = 'Looping thru bags. Minting & Binding new ARKs'
    log.addEntry(msg)
    for bag in bags:
        msg = 'Bag:'+bag.getBagName()
        if bag.getPersistentID() == '':
            pid = noid.mint()
            bag.setPersistentID(pid)
            msg += '  Minted PID:'+str(pid) 
            url = cfg.dspaceurlprefix + pid
            noid.bind(pid, url)
            msg += ' Bound URL:'+url
        else:
            msg += ' already has PID:'+str(bag.getPersistentID())
        log.addEntry(msg)
    bagdb.updateBags(bags)
except Exception, e:
    error = 'Error with minting & binding. Halting script.\nSystem error message below:\n' + str(e)
    log.addEntry(error)
    sys.exit()
    
# Instantiate a new XML transformer object and give it the necessary XSLT scripts
try:
    log.addEntry('setting up Transformer object...')
    #transformer = Transformer.Transformer(cfg.qdc2dspace)
    transformer = Transformer.Transformer(cfg.qdc2dspace, cfg.marc2qdc, cfg.mods2qdc, cfg.ead2qdc, cfg.defaultschema, cfg.assumption)
    log.addEntry('success')
except Exception, e:
    error = 'Error setting up Transformer object. Halting script.\nSystem error message below:\n' + str(e)
    log.addEntry(error)
    sys.exit()

# Instantiate a BagIt-to-DSpaceItem converter object
try:
    log.addEntry('setting up Converter object...')
    converter = Converter.Converter()
    converter.setTransformer(transformer)
    converter.setAssetStoreList(cfg.assetstorelist)
    converter.setRegister(cfg.register)
    converter.setMetadataPattern(cfg.metadatapattern['path'],cfg.metadatapattern['pattern'])
    converter.setFilePatterns(cfg.filepatterns)
    converter.setMetadataSchema(cfg.defaultschema)
    converter.setLicenseText(cfg.licensetext)
    converter.addBags(bags)
    log.addEntry('success')
except Exception, e:
    error = 'Error setting up Converter object. Halting script.\nSystem error message below:\n' + str(e)
    log.addEntry(error)
    sys.exit()

# Convert Bag objects to DSpace Item objects
try:
    log.addEntry('Converting bags to items...')
    items = converter.convertBags()
    failed=converter.getFailures()
    msg = 'Total bags:'+str(len(bags))+'   Converted:'+str(len(items))+'   Failed:'+str(len(failed))
    log.addEntry(msg)
    if len(failed) > 0:
        log.addEntry('Failed Bags:\n')
        for bag in failed:
            log.addEntry(bag.getBagName())
except Exception, e:
    error = 'Error converting bags to items. Halting script.\nSystem error message below:\n' + str(e)
    log.addEntry(error)
    sys.exit()


# Instantiate DSpace Simple Archive object
try:
    log.addEntry('Building Simple Archive Format...')
    saf = SimpleArchive.SimpleArchive(cfg.workbenchpath, items=items)
    saf.buildSimpleArchive()
    log.addEntry('success')
except Exception, e:
    error = 'Error building Simple Archive Format. Halting script.\nSystem error message below:\n' + str(e)
    log.addEntry(error)
    sys.exit()


# Call DSpace import command
try:
    log.addEntry('Importing...')
    args = []
    args.append(cfg.dspacepath + "bin/dspace")
    args.append("import")
    args.append("--add")
    args.append("--eperson="+cfg.eperson)
    args.append("--collection=14")
    args.append("--source="+saf.getBatchDir().rstrip('/'))
    args.append("--mapfile="+cfg.workbenchpath+saf.getName()+"_mapfile")
    output = sub.call(args)
    outputmsg = 'command output:'+str(output)
    log.addEntry(outputmsg)
    if output > 0:
        raise Exception, 'Error with import command'
    log.addEntry('import successful')
except Exception, e:
    error = 'Error importing. Halting script.\nSystem error message below:\n' + str(e)
    log.addEntry(error)
    sys.exit()

# Update bags in DB
try:
    log.addEntry('updating bags in DB')
    for bag in bags:
        bag.setBagStatus('imported')
        bag.setImportedOn(imported_on)
    for bag in failed:
        bag.setBagStatus('failed')
    bagdb.updateBags(bags)
    log.addEntry('Bags successfully updated in DB')
except Exception, e:
    error = 'Error updating bag status. Halting script.\nSystem error message below:\n' + str(e)
    log.addEntry(error)
    sys.exit()
