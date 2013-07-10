# DSpace Simple Archive Format Builder Class
# This class creates the temporary directory for the DSpace ingest process,
# and loads the subdirectories for each item with the necessary files, including:
#   - The contents file
#   - The handle file
#   - The dublin_core.xml file

import subprocess
import datetime
import libxml2
import libxslt
import urllib


class SAFBuilder():

    # Initialize class attributes
    # workspace = '/home/dspace/dock'  # ???Is the DSpace directory a good place for this?
    workspace = /home/jngomez/dock
    assetstore = 1
    noid_url = "http://localhost/nd/noidu_tsthdl"  # TODO: update this url to noid production server


    # Modular methods section
    # These are used in the main fullBuild() method, but can be used independently by other scripts too

    def createBatchDir():
        # Call this to create the temporary SAF directory
        try:
            dt = datetime.datetime.now()
            dir_name = workspace + "/importbatch-" + str(dt.date()) + "-" + str(dt.time())   # directory names will be formatted like this: "importbatch-2010-08-01-12:35:04.765000"
            subprocess.call(["mkdir",dir_name])
            return dir_name
        except Exception, err:
            error_message = 'Error creating batch directory.\nError Message: ' + str(err) + '\n'
            print error_message
            raise Exception, error_message

    def createSubdir(dir_name, barcode):
        # Call this to create an item subdirectory
        try:
            subdir_name = dir_name + "/item_" + barcode     # subdirectory formatted like: "item_44715638056086"
            subprocess.call(["mkdir",subdir_name])
            print 'Created item subdirectory ' + subdir_name
            return subdir_name
        except Exception, err:
            error_message = 'Error creating subdirectory for item ' + barcode + '.\nError Message: ' + str(err) + '\n'
            print error_message
            raise Exception, error_message

    def createContentsFile(subdir_name, barcode, bag_path):
        # Call this to create the contents file
        try:
            contents = open(subdir_name+"/contents", 'w')

            hi_res_pdf_string = "-r -s " + assetstore + " -f " + bag_path + '/data/PDF/' + barcode + ".pdf"         # hi-res pdf  TODO: change these to more descriptive names
            contents.write(hi_res_pdf_string)

            lo_res_pdf_string = "-r -s " + assetstore + " -f " + bag_path + '/data/PDF/' + output + ".pdf"          # hi-res pdf
            contents.write(lo_res_pdf_string)

            marcxml_string = "-r -s " + assetstore + " -f " + bag_path + '/data/METADATA/' + barcode + "_MRC.xml\tbundle:METADATA"   # MARCXML file
            contents.write(marcxml_string)

            contents.close()
            print "Created contents file for item " + barcode
        except Exception, err:
            error_message = 'Error creating contents file for item ' + barcode + '.\nError Message: ' + str(err) + '\n'
            print error_message
            raise Exception, error_message

    def createHandleFile(subdir_name, barcode):
        # Call this to create the handle file
        try:
            noid_response1 = urllib.urlopen(noid_url + "?mint+1").read()
            pid = noid_response.lstrip('id: ')
            noid_response2 = urllib.urlopen(noid_url + "?bind+set+" + pid + "+item+http://gwdspace.wrlc.org:8180/xmlui/handle/" + pid).read()  #!!! may need to adjust url from xmlui/handle to xmlui/ark, etc.
            handle = open(subdir_name+"/handle","w")
            handle.write(pid)
            handle.close()
            print "Created handle file for item " + barcode
        except Exception, err:
            error_message = 'Error creating handle file for item ' + barcode + '.\nError Message: ' + str(err) + '\n'
            print error_message
            raise Exception, error_message
        
    def createDublinCoreFile(subdir_name, barcode, bag_path):
        try:
            marc_path = bag_path + "/metadata/" + barcode + "_MRC.xml"   # TODO: double check bag structure--path to file
            marc = libxml2.parseFile(marc_path)
            dc = style.applyStylesheet(marc, None)
            style.saveResultToFilename(subdir_name+"/dublin_core.xml", dc, 0)
            marc.freeDoc()
            dc.freeDoc()
            style.freeStylesheet()
            styledoc.freeDoc()
        except Exception, err:
            error_message = 'Error creating Dublin Core file for item ' + barcode + '.\nError Message: ' + str(err) + '\n'
            print error_message
            raise Exception, error_message
        

    # Main method section
    # This is the primary method for building SAFs
    # Call this to run all the functions in a sequence
    
    def fullBuild(items):

        # initialize variables
        errors = 0
        log = ''
        
        try:
            dir_name = createBatchDir()
            
            for item in items:      # For each item in the items list, create directory, contents, handle, and dublin core

                bag_path = item["assest_store_path"] + item["project_name"] + '/' + item["bag_name"]
                barcode = item["barcode"]

                try:
                    log += "Creating subdirectory for item " + barcode + "\n"
                    subdir_name = createSubdir(dir_name, barcode)
                    log += "Subdirectory successfully created\n"

                    log += "Creating contents file\n"
                    createContentsFile(subdir_name, barcode, bag_path)
                    log += "Contents file successfully created\n"

                    log += "Creating handle file\n"
                    createHandleFile(subdir_name, barcode)
                    log += "Handle file successfully created\n"

                    log += "Creating Dublin Core file\n"
                    createDublinCoreFile(subdir_name, barcode, bag_path)
                    log += "Dublin Core file successfully created\n"
                    
                except Exception, err:
                    errors += 1
                    log += str(err) + "\nSkipping item " + barcode + "\n\n"
                    continue

                log += "Successfully created SAF for item " + barcode + "\n\n"
                # end for loop

        except Exception, err:
            error_message = "Could not create batch directory.\nError message:" + str(err) + "\n\n"
            raise Exception, error_message

        total = items.count() - errors
        print str(total), "item directories built\n", errors, "errors"
        logfile = open("log.txt","w")
        logilfe.write(log)
        logfile.close()

        
        

        
