# Module to import directries or files

import urllib2
import json
import pprint
import re
import os
import sys
import xml.etree.ElementTree as ET




class importer() :
    
    def __init__(self) :
        self.dir = None
        self.file = None
        self.files = []

    def checkDir(self) :
        return os.path.isdir( self.dir ) , None
    
    def checkFile(self):        
        return os.path.isFile( self.file ) , None
        
    def findFiles(self,suffix) :
       
       # Initialize error
       err = None
       
       if not suffix :
           err = 'Missing file suffix'
           
       if self.dir and self.checkDir :
           for root, dirs, files in os.walk(self.dir):
               for file in files:
                   if suffix and not file.endswith(suffix):
                       pass
                   else:
                       self.files.append( os.path.join(root,file) )
       else :
           print "Can't execute findFiles, no valid directory: %s" , self.dir
           err = 'No directory ' + self.dir
       return self.files , err