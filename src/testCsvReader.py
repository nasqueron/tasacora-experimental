#!/usr/bin/python

from csvReader import *

#-----------------------------------
# Management of arguments
#-----------------------------------
import argparse
parser = argparse.ArgumentParser(
    description='test of cvsReader: takes CSV files as argument; pretty-print them in standard output.')
# positional argument
parser.add_argument(
    "infiles",
    nargs='+',
    help="filenames of the CSV files against which to test csvReader.")

args = parser.parse_args()


# -----------------------------------
# Main
# -----------------------------------
for infile in args.infiles:
    #csvData = open(infile, 'r').read()
    
    csvData = csvReader(infile)
    csvData.prettyPrint()
    