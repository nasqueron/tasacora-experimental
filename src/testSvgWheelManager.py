#!/usr/bin/python

from svgWheelManager import *

#-----------------------------------
# Management of arguments
#-----------------------------------
import argparse
parser = argparse.ArgumentParser(
    description='test of svgColourManager: takes SVG maps as argument; should return a the code of a SVG map with superimposed charts, in standard output.')
# positional argument
parser.add_argument(
    "infiles",
    nargs='+',
    help="filenames of the SVG files against which to test svgColourManager.")

args = parser.parse_args()


# -----------------------------------
# Main
# -----------------------------------
for infile in args.infiles:
    svg = open(infile, 'r').read()

    #import xml.etree.cElementTree as ET
    #tree = ET.ElementTree(ET.fromstring(svg))

    # for node in tree.findall('.//{%s}path' % SVG_NS):
    #svg = insertCircleOnPath(node)

    ##print (svg)

    wheelManager = SvgWheelManager(svg)
    # wheelManager.insertCirclesOnPaths()
    # wheelManager.insertRectAroundPaths()
    wheelManager.insertCircleChartOnPaths()

    wheelManager.printSVG()
