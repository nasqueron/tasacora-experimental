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

    for i in treeManager.findPath("gb-gbn"):
        #print ("-------")
        #print (i)
        #print (treeManager.findParent(i))
        #print (treeManager.findParents(i))
        
        #m = [1,0,0,1,0,0]
        #for j in treeManager.findParents(i):
            ##print ( "   ", toMatrix( treeManager.getTransform(j) ) )
            #n = toMatrix( treeManager.getTransform(j) )
            #m = multiplySvgMatrices (n, m)
        #print (m)
        
        print ( treeManager.getParentsTransformMatrix(i) )
        print ( treeManager.getTransformMatrix(i)        )
        print ( treeManager.getTotalTransformMatrix(i)   )
    
    
    