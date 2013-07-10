bagsinspace
===========

A script for importing bags into DSpace



We import bags to dspace using the batch import function:

$: /home/dspace/bin/dspace import 

However, to import this way, the data must be organized into a Simple Archive Format, which is a prescribed set of directories and files that DSpace will look for.  The Importer uses the SAFBuilder to build the top level directories of the SAF.

Importer reads data from the bagdb and creates Bag objects from the db rows.  It then converts the Bag objects to Item objects, which involves creating ARKs for items that do not already have one. The Item objects create their own subdirectories in the SAF and use the metadata to create the associated files. The Items then rely on the Transformer script to convert the Marc or simple Dublin Core files to extended Dublin Core, which is finally transformed into DSpace's own brand of Dublin Core.  This is done using the xslt scripts.

The Items also scan the bag for pdf directories and add the found pdfs to the list of bitstreams in its "contents" file.

Additionally, Items create a "handle" file which contains the item's unique identifier. In our case, we are feeding DSpace ARKs instead of handles.

Once each bag has created its own subdir in the SAF, the Importer calls the dspace import function and points it at the SAF it has built.
