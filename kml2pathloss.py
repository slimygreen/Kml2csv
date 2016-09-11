#!/usr/bin/env python
# encoding: utf-8
"""

kmlsites-pathloss.py version 1.2 7/9/2016 - created by brendan moss.

converts sites from KML to pathloss links and sites as separate csv's for easy importation into pathloss
"""

import os
import csv
import getpass
import logging
from optparse import OptionParser

from bs4 import BeautifulSoup
"import gdata.docs.service"
"import gdata.docs.data"


class KmlParser(object):
    """
        KmlParser
        
    """ 
    def __init__(self, kmlfile, csvsitesfile, csvlinksfile):
        self.kmlfile = kmlfile
        self.csvsitesfile = csvsitesfile
        self.csvlinksfile = csvlinksfile
        self.outputlinksfile = ''
        self.outputsitesfile = ''
        self.outputdatalinks = []
        self.outputdatasites = []
    
    def ParseKml(self): 
        """
            parse_kml
        """
        try:
            handler = open(self.kmlfile).read()
            #soup = BeautifulSoup(handler)
            folders = BeautifulSoup(handler, "html.parser")
            locationdata = []
            linkdata = []
                      

            for message in folders.find_all('placemark'):
                name = message.find('name')
                name = name.string
                name = name.rstrip('\n')
                
                pointstring = message.find('point')
                linestring = message.find('linestring')
                if linestring: #check if linestring (link!) in placemark
                    #print("linestring =",linestring,"\n")
                    coordinates = message.find('coordinates')
                    coords = coordinates.string
                    coords=coords.replace('\n',',')
                    coords = coords.split(',')                         
                    coords.insert(0, name)
                    coords.pop(1)
                    
                    #coords.pop(7)
                    #print ('links = ', coords,'\n')

                    linkdata.append(coords)


                if    pointstring: #check if pointstring (site!) in placemark
                      #print("pointstring =",pointstring,"\n")
                      coordinates = message.find('coordinates')
                      coords = coordinates.string
                      coords = coords.split(',')                         
                      coords.insert(0, name)
                      #print ('sites = ', coords,'\n')
                      locationdata.append(coords)

                   
            self.outputdatasites = locationdata
            self.outputdatalinks = linkdata

        except OSError as strerror:
           print("OS error")

    def WriteCsv(self):
        """
            write_csv        
        """ 
        self.outputsitesfile = os.getcwd() + '/' + self.csvsitesfile
        self.outputlinksfile = os.getcwd() + '/' + self.csvlinksfile
        try:
            outsites = open(self.outputsitesfile,'w')
            outlinks = open(self.outputlinksfile,'w')
            print(('Writing output of sites to file'), self.outputsitesfile,"\n")
            print(('Writing output to links file'), self.outputlinksfile,"\n")
            
            try:
                writersites = csv.writer(outsites, dialect = 'excel', quoting=csv.QUOTE_NONNUMERIC)
                writerlinks = csv.writer(outlinks, dialect = 'excel', quoting=csv.QUOTE_NONNUMERIC)
                print ("No. of sites = ", len(self.outputdatasites),'\n')
                print ("No. of links = ", len(self.outputdatalinks),'\n')
                #print (self.outputdatasites)
                
                for row in self.outputdatasites:
                    writersites.writerow(row)
                    #print (row)

                for row in self.outputdatalinks:
                    writerlinks.writerow(row)
                    #print (row)
                    
                print(('Output file '), self.outputsitesfile, ' written')
                print(('Output file '), self.outputlinksfile, ' written')
                           
            finally:
                outsites.close()
                outlinks.close()

        except OSError as strerror:
           print("OS error writing file")

        return self.outputsitesfile

def main():
    """
        Main method
    """
    parser = OptionParser()
    parser.add_option("-f", "--file", dest = "kmlfile", 
                    help = "KML file to be parsed", 
                    metavar = "FILE")                     
    parser.add_option("-d", "--output", dest = "csvfile", 
                   help = "CSV output file", 
                   metavar = "FILE")
    (options, args) = parser.parse_args()
    if not options.kmlfile:
        kmlfile = input("Enter kml file name WITHOUT extension: ")
        csvsitefile=kmlfile +'sites.csv'
        csvlinkfile=kmlfile +'links.csv'
        kmlfile = kmlfile +'.kml'
        print("destination file will be ", csvsitefile)
    elif not options.csvfile:
        csvsitefile=kmlfile +'sites.csv'
        csvlinkfile=kmlfile +'links.csv'
        kmlfile =kmlfile + '.kml'
        
    else:
        kmlfile=options.kmlfile
        csvsitefile=options.csvfile
        csvsitefile=kmlfile +'sites.csv'
        csvlinkfile=kmlfile +'links.csv'
    
    kmlparser = KmlParser(kmlfile, csvsitefile, csvlinkfile)               
    kmlparser.ParseKml()
    upload_file = kmlparser.WriteCsv()
    #kmlparser.Upload(upload_file)

if __name__ == "__main__":
    main()




 
