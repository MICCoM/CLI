import urllib2
import json
import pprint
import re
import os
import sys
import mio
import model
import xml.etree.ElementTree as ET
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import jsonpickle



def md5(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

class handle:

    def __init__(self, api, dataDir, code):
        self.api = api
        self.dir = dataDir
        self.code = code
        self.files = []
        self.nodes = []
        self.suffix = None
        self.graph = None



    def findFiles(self):
        nodes = []
        for (root, dirs, files,) in os.walk(dataDir):
            for file in files:
                if file.endswith('.r'):
                    print os.path.join(root, file)
                    self.files.append(os.path.join(root, file))
                    addNodes(nodes, os.path.join(root, file), root)


        self.nodes = nodes
        return err



    def addNodes(nodes, fname, path):
        tree = ET.parse(fname)
        root = tree.getroot()
        regexpFlags = re.compile('species|save')
        regexpFilename = re.compile('\\S+$')
        regexpSpecies = re.compile('species (\\S+)')
        node = {'name': fname,
         'parents': [],
         'children': []}
        for child in root:
            if child.tag == 'cmd':
                m = regexpFlags.match(child.text)
                if m:
                    if m.group() == 'species':
                        f = regexpFilename.search(child.text)
                        s = regexpSpecies.match(child.text)
                        print 'File',
                        print f.group()
                        print 'Species Name',
                        print s.group(1)
                        node['parents'].append(f.group())
                    if m.group() == 'save':
                        f = regexpFilename.search(child.text)
                        node['children'].append(path + '/' + f.group())
                        print 'Out:',
                        print f.group()

        nodes.append(node)
        return nodes



    def createGraph(self):
        G = nx.Graph()
        val_map = {}
        if self.nodes:
            for node in self.nodes:
                G.add_node(node['name'], type='Master')
                val_map[node['name']] = '2.5'
                for c in node['children']:
                    G.add_node(c, type='Output')
                    G.add_edge(c, node['name'])
                    val_map[c] = 0.25

                for p in node['parents']:
                    G.add_node(p, type='Input')
                    G.add_edge(p, node['name'])
                    val_map[p] = 0.25


        else:
            print 'No nodes'
        values = [ val_map.get(nname, 0.25) for nname in G.nodes() ]
        self.gvalues = values
        self.graph = G



    def exportGraph(self, format, label_type, node_label_attribute, edge_label_attribute, outdir, outname):
        G = self.graph
        pos = nx.spring_layout(G)
        nx.draw(G, pos, cmap=plt.get_cmap('jet'), node_color=values)
        if label:
            if label == 'node' or label == 'both':
                if not node_label_attribute:
                    node_label_attribute = 'type'
                node_labels = nx.get_node_attributes(G, node_label_attribute)
                nx.draw_networkx_labels(G, pos, labels=node_labels)
            if label == 'edge' or label == 'both':
                if not edge_label_attribute:
                    node_label_attribute = 'type'
                edge_labels = nx.get_edge_attributes(G, edge_label_attribute)
                nx.draw_networkx_edge_labels(G, pos, labels=edge_labels)
        else:
            print 'Exporting graph without labels'
        if format == 'png':
            fname = os.path.join(outdir, outname)
            plt.savefig(fname)
            return fname
        if format == 'json':
            ndata = json_graph.node_link_data(G)
            return json.dumps(ndata)
        print "Don't recognize format: " + format


    def createExperiment(self) :
        
        err = None
        i   = mio.importer()
       
        # temporary variable , place holder for file or directory
        file_or_dir = self.dir
        
        # Check if file or dir
        if os.path.isdir(file_or_dir) :
            i.dir = file_or_dir
        elif os.path.isFile(file_or_dir):
            i.file = file_or_dir
        i.file = file_or_dir
        
        # Find all files with suffix if importing dir
        if i.dir :
            files , err = i.findFiles(self.suffix)
            if err :
                sys.stderr.write( err + "\n")
                sys.stderr.write( "\n".join(files))
            else :
                print "Creating Experiment"
                experiment = model.Experiment()
                experiment.createFromFiles(files , self.code)
                return experiment , None
                
        return None , err

    def toJson(self, data) :
        print data
        return jsonpickle.encode(data , unpicklable=False)
        # return json.dumps(data)
    

if __name__ == '__main__':
    import sys
    print 'Running as script'

