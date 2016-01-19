#!/usr/bin/env python

import os
import sys
import json
import time
import base64
import MICCOM
import MICCOM.miccom
import MICCOM.mio
from operator import itemgetter
from optparse import OptionParser
from prettytable import PrettyTable
#from MICCOM import *



def main():
    print "# Welcome"
    parser = OptionParser( usage='miccom import DIRECTORY')
    #parser.add_option("import",  dest="importer", default="", help="import an experiment")
    parser.add_option("-s", "--search", dest="search", default="", help="search terms")
    #parser.add_option("-h", "--help", dest="help", default="", help="help options")
    parser.add_option("-i", "--import", dest="importer", default="", help="import an experiment")
    parser.add_option("-c", "--create", dest="create", default="", help="create an experiment file")
    parser.add_option("-e", "--export", dest="export", default="", help="export an experiment")
    parser.add_option("-v", "--validate", dest="validate", default="", help="validate an experiment")
    parser.add_option("-d", "--directory", dest="dirname", default="", help="directory to read data from")
    parser.add_option( "--file", dest="filename", default="", help="filename")
    parser.add_option("-x", "--suffix", dest="suffix", default="", help="file suffix for directory search")
    parser.add_option("-f", "--format", dest="format", default="", help="input or output format (e.q. input: qbox , output: png , json)")
    (opts, args) = parser.parse_args()


    
        

    m = MICCOM.miccom.handle( "http://localhost:8000" , opts.dirname , opts.format)
    
    if not opts.format :
        m.code = "qbox"

    if len(args) < 0:
        sys.stderr.write("ERROR: missing argument. Please check usage with %s -h\n"%(sys.argv[0]))
        return 1
    else:
        pass

    if args :
        if args[0] == "import" :
            print "None"
            # i = MICCOM.importer()
  #
  #           # temporary variable , place holder for file or directory
  #           file_or_dir = opts.importer
  #
  #           if os.path.isdir(file_or_dir) :
  #               i.dir = file_or_dir
  #           elif os.path.isFile(file_or_dir):
  #               i.file = file_or_dir
  #           i.dir = file_or_dir
            
             

    
    if opts.importer :

        print "# Importing " + opts.importer
        # Initialize import from file system methods
        i = MICCOM.mio.importer()
       
        # temporary variable , place holder for file or directory
        file_or_dir = opts.importer
        
        # Check if file or dir
        if os.path.isdir(file_or_dir) :
            i.dir = file_or_dir
        elif os.path.isFile(file_or_dir):
            i.file = file_or_dir
        i.file = file_or_dir
        
        # Find all files with suffix if importing dir
        if i.dir :
            files , err = i.findFiles(opts.suffix)
            if err :
                sys.stderr.write( err + "\n")
                sys.stderr.write( "\n".join(files))
            else :
                print files
            
        # Validate file if importing file
        
        print opts.importer   
        
    if opts.create :
        if opts.create == "experiment" or opts.create == "Experiment" :
            
            if not opts.dirname :
                 sys.stderr.write("Can't create experiment file without directory to parse. Missing option --dir\n")
            else :
                m.dir = opts.dirname
                m.suffix = opts.suffix
                experiment , err = m.createExperiment()
                print experiment
                js = m.toJson(experiment.__dict__)
                print "JSON:"
                print js   
                           

    print opts.search
    return 0

if __name__ == "__main__":
    sys.exit( main() )
    #sys.exit( main(sys.argv) )
    