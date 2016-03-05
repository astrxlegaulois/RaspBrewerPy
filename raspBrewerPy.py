#!/usr/bin/python
"""
    Main file for the brewing program
"""

import sys, getopt
import Brewer

def main(argv):
   configfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hc:o:",["cfile=","ofile="])
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

if __name__ == "__main__":
   main(sys.argv[1:])
   the_brewer=Brewer()
   the_brewer.config_from_file("./config_seb.xml")
