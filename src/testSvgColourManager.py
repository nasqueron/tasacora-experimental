#!/usr/bin/python

from svgColourManager import SvgColourManager



#-----------------------------------
# Management of arguments
#-----------------------------------
import argparse
parser = argparse.ArgumentParser(description='test of svgColourManager: takes SVG maps as argument; sould return a list of ID tags and matching colours in standard output.')
# positional argument
parser.add_argument("infiles", nargs='+', help="filenames of the SVG files against which to test svgColourManager.")
      
args = parser.parse_args()


##-----------------------------------
## Main
##-----------------------------------
for infile in args.infiles:
    #print("Reading from "+infile+".")
    svg = open(infile, 'r').read()
    colourManager = SvgColourManager(svg)
    colourManager.colourAllRandom()
    #colourManager.listTagsAndColours()
    colourManager.editMap()