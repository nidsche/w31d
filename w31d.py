#!/usr/bin/python
import sys
import io
import re
import os
from os import walk
#from ConfigParser import SafeConfigParser
import ConfigParser
import urllib2
from optparse import OptionParser
from optparse import OptionGroup

## OptionParser
options = OptionParser(usage='%prog Target_Definition', version="%prog 0.0", description='Identify applications running on a webserver')
group1 = OptionGroup(options,"Target definitions")
group1.add_option('--url', '-u', dest="url", default=[], action="append", help="URL to test")
group1.add_option("--brute-dir", action="store_true", dest="brute_dir", default=False, help="Try to bruteforce directories")
group1.add_option("--brute-dirlist", dest="brute_dirlist", default='',  help="Try to bruteforce directories")
group1.add_option("--store-in-db", action="store_true", dest="store-in-db", default=False, help="store inside database (not implemented)")
group1.add_option("--check-vulns", action="store_true", dest="check-vulns", default=False, help="check for vulnerabilities")
group1.add_option("--list-plugins", action="store_true", dest="listPlugins", default=False, help="List available plugins")
options.add_option_group(group1)
opts, args = options.parse_args()

## Default Config Section
config = ConfigParser.SafeConfigParser(defaults = {'user-agent': 'Mozilla/5.0'})

alphabet="abcdefghijklmnopqrstuvwxyz0123456789"

fdlist=[]
pluginList={}

debug_lvl=20
normalHeaders={}

tval=''

def loadPlugins(directory="plugins/"):
    # XXX read directory
    if debug_lvl > 19:
        print "Loading plugins (not fully implemented)"
        print "Plugins: Checking Directory "+directory
    # load all python files (extension py)
    f = []
    for (dirpath, dirnames, filenames) in walk(directory):
        for fn in filenames:
            if fn.endswith(".py"):
                f.append(fn)
        break
    if debug_lvl > 19:
        print "List of available plugins: "
        print f
    # add to pluginList
    sys.path.append("plugins/")
    for pn in f:
        # There might be an issue about the filename
        pn = pn.replace(".py","")
        print "Loading: " +pn
        plug = __import__(pn)
        pluginList[pn]=plug.Plugin()
        print pluginList[pn].getName()
	print pluginList[pn].getter()
	pluginList[pn].setter("jibbi"+pn)
	print pluginList[pn].getter()
    return

def readConfig():
    #print config.get('user-agent')
    if debug_lvl >10:
        print "Dummy reading config"

def testCall():
    print "Hello World"

def checkOptions(myurl):
    if debug_lvl  >10:
        print "CheckOptions: To be implemented"

def evaluateHeader(header):
    if debug_lvl  >20:
        print "evaluateHeader: To be implemented"
    for line in str(header).split("\n"):
        #print "##" + line
        gp = line.find(":")
        if gp > 0:
            key = line[0:gp]
            val = line[gp+2:]
            #print key+"#"+val
            if key in normalHeaders:
                pass
            else:
                normalHeaders[key]=val
    print header



def retrieveUrl(myurl,  ref='NONE'):
    req = urllib2.Request(myurl)
    # XXX here we need to use the value from config
    req.add_header('User-Agent', config.defaults()['user-agent'])
    if ref != 'NONE':
        req.add_header('Referer', ref)
    response = urllib2.urlopen(req)
    evaluateHeader(response.info())
    return response

def handleErrorCode(url,  e):
    if e.code==401:
        print "Credential required"
        print e.info()
    elif e.code==403:
        print "Found forbidden URL: "+url
        fdlist.append(url)
    elif e.code==404:
        pass
    else:
        print "Unhandeled Error Code: " + str(e.code)
        print e.getcode()
        print e.info()
        evaluateHeader(e.info())

def bruteDir(myurl,  depth):
    if depth==0:
        if debug_lvl>20:
            print "trying "+myurl
        try:
            res = retrieveUrl(myurl)
            if res.getcode() == 200:
                print "Found " +myurl
                fdlist.append(myurl)
        except urllib2.HTTPError as e:
            handleErrorCode(myurl,  e.code)
        try:
            res = retrieveUrl(myurl+"/")
            if res.getcode() == 200:
                print "Found " +myurl+"/"
                fdlist.append(myurl+"/")
        except urllib2.HTTPError as e:
            handleErrorCode(myurl+"/",  e)
    else:
        for i in alphabet:
            bruteDir(myurl+i,  depth-1)

def printResults():
    printFilesFound()
    printHeadersFound()
    
def printHeadersFound():
    for key in normalHeaders:
        print key +" -> "+normalHeaders[key]

def printFilesFound():
    print "Found the following Files/Directories"
    for i in fdlist:
        print i

def listPlugins():
    print "Active Plugins"
    for p in pluginList:
        print pluginList[p].getName()
	print pluginList[p].getter()

def main():
    readConfig()
    # XXX make this configurable
    scriptDir =  os.path.realpath(__file__).replace("w31d.py", "")+"plugins/"
    #print scriptDir
    loadPlugins(scriptDir)
    print opts.url
    for url in opts.url:
        if opts.brute_dir:
            j=0
            while True:
                print "Bruting "+url+" depth "+str(j)
                bruteDir(url, j)
                j=j+1
        if len(opts.brute_dirlist) > 0:
            fi = open(opts.brute_dirlist, "r")
            for line in fi:
                line=line.replace("\n","")
                line=line.replace("\r","")
                if(len(line)>0):
                    if line[0]=="#":
                        pass
                    else:
                        #print url+line
                        bruteDir(url+line, 0)
        try:
            res = retrieveUrl(url)
            print res.getcode()
            print res.info()
        except urllib2.HTTPError as e:
            handleErrorCode(url+"/",  e)
    printResults()
    if opts.listPlugins:
        listPlugins()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print "Cancelled by user"
        printFilesFound()
