#!/usr/bin/python

from svgTreeManager import *

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
    svg = open(infile, 'r').read()
    
    treeManager = SvgTreeManager(svg)

    #target = "gb-gbn"
    #target = "de"
    #target = "ddr"    
    target = "so"
    for i in treeManager.findPath(target):
        print ( " ==== ", i.get('id'), " ==== ")
        print ( treeManager.getParentsTransformMatrix(i) )
        print ( treeManager.getTransformMatrix(i)        )
        print ( treeManager.getTotalTransformMatrix(i)   )
        print ( "Path points: ", treeManager.extractPoints(i) )
    
    
    