#!/usr/bin/python

from idTagDetector import IdTagDetector


#-----------------------------------
# Management of arguments
#-----------------------------------
import argparse
parser = argparse.ArgumentParser(
    description='test of idTagDetector: takes SVG maps as argument; sould return a list of ID tags used in the file to designate continents, countries, administrative subdivisions, etc. in standard output.')
# positional argument
parser.add_argument(
    "infiles",
    nargs='+',
    help="filenames of the SVG files against which to test idTagDetector.")

args = parser.parse_args()


#-----------------------------------
# Main
#-----------------------------------
for infile in args.infiles:
    print("Reading from " + infile + ".")
    svg = open(infile, 'r').read()
    detector = IdTagDetector(svg)
    detector.detect()
    detector.listTags()
