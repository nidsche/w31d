#!/usr/bin/python
import sys
import io
import re
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
group1.add_option("--brute-dirlist", dest="brute_dirlist", default=False, help="Try to bruteforce directories")
options.add_option_group(group1)
opts, args = options.parse_args()

## Default Config Section
config = ConfigParser.SafeConfigParser(defaults = {'user-agent': 'Mozilla/5.0'})

alphabet="abcdefghijklmnopqrstuvwxyz0123456789"

fdlist=[]

debug_lvl=20

def readConfig():
    #print config.get('user-agent')
    if debug_lvl >10:
        print "Dummy reading config"

def loadPlugins():
    if debug_lvl  >10:
        print "Dummy loading plugins"

def checkOptions(myurl):
    if debug_lvl  >10:
        print "CheckOptions: To be implemented"

def evaluateHeader(header):
    if debug_lvl  >10:
        print "evaluateHeader: To be implemented"



def retrieveUrl(myurl,  ref='NONE'):
    req = urllib2.Request(myurl)
    # XXX here we need to use the value from config
    req.add_header('User-Agent', config.defaults()['user-agent'])
    if ref != 'NONE':
        req.add_header('Referer', ref)
    response = urllib2.urlopen(req)
    return response

def handleErrorCode(url,  code):
    if code==403:
        print "Found forbidden URL: "+url
        fdlist.append(url)
    elif code==404:
        pass
    else:
        print "Unhandeled Error Code: " + str(code)

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
            handleErrorCode(myurl+"/",  e.code)
    else:
        for i in alphabet:
            bruteDir(myurl+i,  depth-1)

def printFilesFound():
    print "Found the following Files/Directories"
    for i in fdlist:
        print i

def main():
    readConfig()
    #loadPlugins()
    print opts.url
    for url in opts.url:
        #res = retrieveUrl(url)
        #print res.getcode()
        #print res.info()
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

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print "Cancelled by user"
        printFilesFound()
