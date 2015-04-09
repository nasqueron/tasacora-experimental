from idTagDetector import IdTagDetector
from svgTreeManager import *
SVG_NS = "http://www.w3.org/2000/svg"



 
# Inserts a circle in a SVG. Returns the SVG as a string. For testing mostly.
# Example of SVG circle syntax:
#           <circle cx="600" cy="200" r="100" fill="red" stroke="blue" stroke-width="10"  />
def insertCircle(svgData, centreX, centreY, radius="10", strokeWidth="1", fillColour="red", strokeColour="blue", circleID=""):
    import re
    
    regex = re.compile("(.*)(</svg>)", re.DOTALL)
    m = regex.match(svgData)
    
    svgData = m.group(1)
    svgData = svgData+"\n<circle cx=\""+str(centreX)+"\" cy=\""+str(centreY)+"\" r=\""+str(radius)+"\" fill=\""+fillColour+"\" stroke=\""+strokeColour+"\" stroke-width=\""+str(strokeWidth)+"\" id=\""+circleID+"\"  />"
    svgData = svgData+"\n"+m.group(2) 
    return svgData
    
# Inserts a Rect in a SVG. Returns the SVG as a string. For testing mostly.
# Example of SVG rect syntax:
#           <rect x="50" y="20" width="150" height="150" style="fill:blue;stroke:pink;stroke-width:5;fill-opacity:0.1;stroke-opacity:0.9" />
def insertRect(svgData, xMax, yMax, xMin, yMin, strokeWidth="2", fillColour="none", strokeColour="green", rectID=""):
    import re
    
    regex = re.compile("(.*)(</svg>)", re.DOTALL)
    m = regex.match(svgData)
    
    svgData = m.group(1)
    leftPosition = xMin
    topPosition  = yMin
    height       = yMax - yMin
    width        = xMax - xMin
    
    #strokeWidth = 2
    
    svgData = svgData+"\n<rect x=\""+str(leftPosition)+"\" y=\""+str(topPosition)+"\" height=\""+str(height)+"\" width=\""+str(width)+"\" fill=\""+fillColour+"\" stroke=\""+strokeColour+"\" stroke-width=\""+str(strokeWidth)+"\" id=\""+rectID+"\"  />"
    svgData = svgData+"\n"+m.group(2) 
    return svgData


# Class to generate percentage Wheels
class SvgWheelManager:
    def __init__(self, arg):
        self.inputSVG             = arg
        self.tagsAndAbsolueValues = {}
        self.tagsAndPercentage    = {}
        self.listOfIDs            = self.fillListOfIDs()
        self.treeManager          = SvgTreeManager(self.inputSVG)

    # Just used in constructor to fill self.listOfIDs
    def fillListOfIDs(self):
        from idTagDetector import IdTagDetector
        detector = IdTagDetector(self.inputSVG)
        detector.detect()
        return detector.detectedTags   
    
    # gives a size to annotation circles based on viewport size.
    def defaultCircleRadius(self):
        radius = self.treeManager.characteristicDimensions()/200.0
        return radius    
    
    # gives a width to annotation lines based on viewport size.
    def defaultLineWidth(self):
        radius = self.treeManager.characteristicDimensions()/600.0
        return radius    
    
    # Inserts an SVG circle on the barycentre of the path given as argument
    def insertCircleOnPath(self, path):
        pathID = self.treeManager.getNodeID(path)
        if not "path" in pathID:
            #print(pathID)
            cx = (self.treeManager.centreOfMass(path))[0]
            cy = (self.treeManager.centreOfMass(path))[1]
            self.inputSVG = insertCircle( self.inputSVG, cx, cy, radius=self.defaultCircleRadius(), circleID="circle-"+pathID)
        
    def insertCirclesOnPaths(self):
        for node in self.treeManager.findPath():
            self.insertCircleOnPath(node)
        #tree = ET.ElementTree(ET.fromstring(self.inputSVG))
        #for node in tree.findall('.//{%s}path' % SVG_NS):
            #self.insertCircleOnPath(node)
        
    def insertRectAroundPath(self, path):
        pathID = self.treeManager.getNodeID(path)
        if not "path" in pathID:
        #if "fr" in pathID:
            xMax = max( (self.treeManager.extractPoints(path))[0] )
            xMin = min( (self.treeManager.extractPoints(path))[0] )
            yMax = max( (self.treeManager.extractPoints(path))[1] )
            yMin = min( (self.treeManager.extractPoints(path))[1] )

            #self.inputSVG = insertRect( self.inputSVG, xMax, yMax, xMin, yMin, rectID="rect-"+pathID)
            #self.inputSVG = insertRect( self.inputSVG, xMax, yMax, xMin, yMin, rectID="rect-"+pathID, strokeWidth="40" )
            self.inputSVG = insertRect( self.inputSVG, xMax, yMax, xMin, yMin, rectID="rect-"+pathID, strokeWidth=self.defaultLineWidth() )

    
    def insertRectAroundPaths(self):
        for node in self.treeManager.findPath():        
            self.insertRectAroundPath(node)        
        #tree = ET.ElementTree(ET.fromstring(self.inputSVG))
        #for node in tree.findall('.//{%s}path' % SVG_NS):
            #self.insertRectAroundPath(node)
            
    def printSVG(self):
        print(self.inputSVG)    
    
        
    # Reads stuff from an actual data read that we will have to build.
    #def fillTagsAndAbsolueValues(self):
        #for i in self.listOfIDs:
        
    #Fills self.tagsAndAbsolueValues with random stuff for testing
    def randomTagsAndAbsolueValues(self):
        import random
        for i in self.listOfIDs:
            self.tagsAndAbsolueValues[i] = random.randint(0, 16777215)
            
    #Fills self.tagsAndPercentage with percentage of total, as in localValue/Sum(localValues)
    def fillTagsAndPercentageOfTotal(self):
        totalValue = sum(self.tagsAndAbsolueValues.values())
        for i in self.tagsAndAbsolueValues.keys():
            self.tagsAndPercentage[i] = self.tagsAndAbsolueValues[i]*100.0/fillTagsAndPercentageOfTotal
            
    # Fill with different sorts of percentage later.
    
    
    