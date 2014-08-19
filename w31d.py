#!/usr/bin/python
import sys
import io
#from ConfigParser import SafeConfigParser
import ConfigParser
import urllib2
from optparse import OptionParser
from optparse import OptionGroup

## OptionParser
options = OptionParser(usage='%prog Target_Definition', version="%prog 0.0", description='Identify applications running on a webserver')
group1 = OptionGroup(options,"Target definitions")
group1.add_option('--url', '-u', dest="url", default=[], action="append", help="URL to test")
options.add_option_group(group1)
opts, args = options.parse_args()

## Default Config Section
config = ConfigParser.SafeConfigParser(defaults = {'user-agent': 'Mozilla/5.0'})

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



def main():
    readConfig()
    #loadPlugins()
    print opts.url
    for url in opts.url:
        res = retrieveUrl(url)
        print res.getcode()
        print res.info()

if __name__ == '__main__':
    main()
