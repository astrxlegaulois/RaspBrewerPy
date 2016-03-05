#!/usr/bin/python
# coding: utf-8
"""
    Main file for the brewing program
"""

import sys, getopt
from brewer import Brewer

if __name__ == "__main__":
    configfile = './config_seb.xml'
    outputfile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hc:o:",["cfile=","ofile="])
    except getopt.GetoptError:
        print 'raspBrewerPy.py -c <configfile> [-o <outputfile>]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'raspBrewerPy.py -c <configfile> [-o <outputfile>]'
            sys.exit()
        elif opt in ("-c", "--cfile"):
            configfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Config file is "',configfile,'"'
    print 'Output file is "',outputfile,'"'
    the_brewer=Brewer()
    the_brewer.config_from_file(configfile)
    print the_brewer.print_self()
    the_brewer.init_brewing()
    the_brewer.brew()
