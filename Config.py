# DSpace Config class file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-10-12

# bagdb values
dbhost = 'localhost'
dbuser = 'bagit'
dbpass = 'GWbaGit'
dbname = 'bagdb'

# NOID url
noidurl = 'http://id.library.gwu.edu'

# dspace url that will be appended with persistent identifiers
dspaceurlprefix = 'http://gwdspace.wrlc.org:8180/xmlui/handle/'

# XSLT scripts
# qualified Dublin Core to DSpace Dublin Core
qdc2dspace = 'gwu-qdc-to-dspacedc.xslt'
# MARC to qualified Dublin Core
marc2qdc = 'gwu-marc-to-qdc.xslt'
# MODS to qualified Dublin Core
mods2qdc = ''
# EAD to qualified Dublin Core
ead2qdc = ''
# ARK inserter for export to Voyager
arkinserter = 'gwu-marc-ark-inserter.xslt'
# BibID & Volume extractor for CSV export to Voyager
bibidfinder = 'gwu-marc-bibid-finder.xslt'

# default metadata schema (choose from: MARC, MODS, EAD)
defaultschema = 'MARC'

# Assumption for main entry type
# See LOC MARC relator code list for possible values
# ***This must be a quote within quotes***
assumption = "'aut'"

# asset store list
# same as listed in dspace config file, index equals number
assetstorelist = ['/home/dspace/assetstore/',
                  '/dspace1/assetstore-ro/']

# Register items or import them into DSpace
register = True

# Pattern for finding and matching primary metadata file
# path is relative to bag directory
# pattern based on UNIX file name matches, not regular expressions
metadatapattern = {'path':'/data/METADATA/', 'pattern':'*_MRC.xml'}

# Patterns for finding and matching files to be included as bitstreams
# path is relative to bag directory
# pattern based on UNIX file name matches, not regular expressions
filepatterns = [{'path':'/data/PDF/', 'pattern':'HighRes_*.pdf', 'bundle':'', 'description':'A high resolution pdf of the book', 'permissions':[]},
                {'path':'/data/PDF/', 'pattern':'LowRes_*.pdf', 'bundle':'', 'description':'A lower resolution pdf of the book for low bandwidth downloads', 'permissions':[]},
                {'path':'/data/METADATA/', 'pattern':'*_MRC.xml', 'bundle':'METADATA', 'description':'Original bibliographic metadata in MARC format', 'permissions':[]}]

# license text
licensetext = 'Most items selected for the Cultural Imaginings project are in the public domain. However, copyrights to some items may be held by creators or their descendants. The Gelman Library at George Washington University respects the interests of copyright holders and encourages them to contact us with questions about participation in this project. Users of these materials are also responsible for compliance with relevant copyright law. '

# location for temporary import files
workbenchpath = '/home/dspace/gw/bagmgmt/workbench/'

# location for exported MARCXML files
exportpath = '/home/dspace/gw/bagmgmt/export-dock/'

# DSpace import parameters
dspacepath = '/home/dspace/'
eperson = 'jngomez@gelman.gwu.edu'
collection = '2'

# paths and file names for script logs
logs = {'validation':'/home/dspace/gw/bagmgmt/log/validation.log',
        'validation_overview':'/home/dspace/gw/bagmgmt/log/validation_overview.log',
        'import':'/home/dspace/gw/bagmgmt/log/import.log',
        'import_overview':'/home/dspace/gw/bagmgmt/log/import_overview.log'}

logDirectories = {'validation':'/home/dspace/gw/bagmgmt/log/validation/',
                  'import':'/home/dspace/gw/bagmgmt/log/import/',
                  'export':'/home/dspace/gw/bagmgmt/log/export/'}



