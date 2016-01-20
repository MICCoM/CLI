# Client view on data model 

import urllib2
import json
import pprint
import re
import os
import sys
import xml.etree.ElementTree as ET

class Experiment() :

    def __init__(self) :
        self.name = None
        self.version = None
        self.codes = []
        self.files = []
        self.workflow = [] # list of steps
        self.author = None
        self.date = None
        self.analysis = None
        self.samples = {}

    def createFromFiles(self, files , format):
        
        err   = None
        steps = []
        nodes = []
        
        if format == "qbox" :
            print "Format " + format + " , reading  files"
            
            for fname in files:
                
                # Create list of file objects and steps
                fobject = File(filename=fname)
                
                self.files.append(fobject)
                
                tree = ET.parse(fname)
                root = tree.getroot()
                regexpFlags = re.compile('species|save')
                regexpFilename = re.compile('\\S+$')
                regexpSpecies = re.compile('species (\\S+)')
                
                step = Step()
                node = {'name': fname,
                 'parents': [],
                 'children': []}
                 
                
                step.code = "qbox"
                step.type = None
                step.script = fobject
 
                for child in root:
                    if child.tag == 'cmd':
                        m = regexpFlags.match(child.text)
                        if m:
                            if m.group() == 'species':
                                f = regexpFilename.search(child.text)
                                s = regexpSpecies.match(child.text)
                                
                                speciesFile = File(filename=f.group())
                                step.input.append(speciesFile)
                                
                                if s.group(1) in self.samples :
                                    self.samples[s.group(1)]+=1
                                else :
                                    self.samples[s.group(1)]= 1
                                    
                                
                                
                                print 'File',
                                print f.group()
                                print 'Species Name',
                                print s.group(1)
                                node['parents'].append(f.group())
                            if m.group() == 'save':
                                f = regexpFilename.search(child.text)
                                
                                #node['children'].append(path + '/' + f.group())
                                node['children'].append(f.group())
                                
                                saveFile = File(filename=f.group())
                                step.output.append(saveFile)
                                print 'Out:',
                                print f.group()

                self.workflow.append(step)
                nodes.append(node)
                        
        else:
            print "Format " + format + " not supported"
        
        return self.files , self.workflow , err
	
	
class Step() :
    
    def __init__(self) :
        self.script = None
        self.code  = None
        self.name  = None
        self.type  = None
        self.categories = []
        self.input = []
        self.output = []
        self.duration = []

class File ():
    
    def __init__(self , filename=None, path=None) :
        self.filename = filename
        self.path = path
        self.md5 = None
        self.size = []
        self.type = None
        self.format = None
        
    

    
class Qbox():
    pass
    
    	