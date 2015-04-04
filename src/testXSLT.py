#!/usr/bin/python

import lxml.etree as ET


#-----------------------------------
# Management of arguments
#-----------------------------------
import argparse
parser = argparse.ArgumentParser(description='test of XSLT')
# positional argument
parser.add_argument("infiles", nargs='+', help="filenames ")
      
args = parser.parse_args()


##-----------------------------------
## Main
##-----------------------------------
for infile in args.infiles:
    #print("Reading from "+infile+".")
    #svg = open(infile, 'r').read()
    svg=infile
    
    dom  = ET.parse(svg)
    xslt = ET.parse("transformation.xslt")
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    output = ET.tostring(newdom, pretty_print=True)
    
    #print("Saving results to "+outfile+"..."),
    outfile = "outgago.svg"
    f = open(outfile,'w')
    f.write(output.decode("utf-8")) # python will convert \n to os.linesep
    f.close() # you can omit in most cases as the destructor will call if