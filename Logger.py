# Log Writer script file
#
# Part of GWU's digitization and preservation solution using BagIt, DSpace, and ARK
#
# Author: Joshua Gomez
# Created: 2010-10-12

import sys
import datetime
import os

class Logger:

    def __init__(self, logpath, addTimeStamp=False, printToScreen=True):

        self.logpath = logpath
        self.printToScreen = printToScreen
        self.addTimeStamp = addTimeStamp
        self.dt = datetime.datetime


    def addEntry(self, entry):
        if self.addTimeStamp:
            timestamp = str(self.dt.now(None))[0:19]
            entry = '[' + timestamp + '] ' + entry
        log = open(self.logpath, 'a')
        log.write(entry)
        log.close()
        if self.printToScreen:
            print entry
