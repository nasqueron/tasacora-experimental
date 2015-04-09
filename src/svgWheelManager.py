from idTagDetector import IdTagDetector
from svgTreeManager import *
import math
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


# Inserts a circle in a SVG. Returns the SVG as a string. For testing mostly.
# Example of SVG circle syntax:
#           <circle cx="600" cy="200" r="100" fill="red" stroke="blue" stroke-width="10"  />
def insertFreeformSvgCode(svgData, SvgCode):
    import re
    
    regex = re.compile("(.*)(</svg>)", re.DOTALL)
    m = regex.match(svgData)
    
    svgData = m.group(1)
    svgData = svgData+"\n" + SvgCode 
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
    
    def getPathHeigth(self, path):
        pathPoints = (self.treeManager.extractPoints(path))[0]
        xMax = max( pathPoints )
        xMin = min( pathPoints )
        return xMax-xMin
    
    def getPathWidth(self, path):
        pathPoints = (self.treeManager.extractPoints(path))[1]
        yMax = max( pathPoints )
        yMin = min( pathPoints )
        return yMax-yMin
    
    def getPathCharacteristicDimension(self, path):
        return min ( self.getPathWidth(path), self.getPathHeigth(path) )
    
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
    
    def insertCircleChartOnPaths(self):
        import random
        for node in self.treeManager.findPath():  
            pathID = self.treeManager.getNodeID(node)
            if "path" in pathID:
                continue
            data = random.randint(0, 99)
            self.insertCircleChartOnPath(node, data)    
            
    def insertCircleChartOnPath(self, path, data):
        
        pathID = self.treeManager.getNodeID(path)
        cx = (self.treeManager.centreOfMass(path))[0]
        cy = (self.treeManager.centreOfMass(path))[1]
        
        mapDim  = self.treeManager.characteristicDimensions()
        pathDim = self.getPathCharacteristicDimension(path)
        magicReadabilityFactor = 8
        if( (pathDim/10) < (mapDim / (10 * magicReadabilityFactor ) ) ):
            pathDim = mapDim/magicReadabilityFactor
        
        outerCircleRadius = pathDim/10
        outerFillColour   = "white"
        outerStrokeColour = "black"
        outerStrokeWidth  =  1
        innerCircleRadius = pathDim/11
        innerFillColour   = "#8484ff"
        innerStrokeColour = "None"
        innerStrokeWidth  =  0
        dataCircleRadius = pathDim/11
        dataFillColour   = "#bdbdff"
        dataStrokeColour = "None"
        dataStrokeWidth  =  0
        
        alpha = 2*math.pi * (data/100)
        X1 = cx
        Y1 = cy
        X2 = cx
        Y2 = cy - dataCircleRadius
        X3 = cx + dataCircleRadius*math.cos(alpha)
        Y3 = cy + dataCircleRadius*math.sin(alpha)
        largeArcFlag = 1
        if (alpha > math.pi): largeArcFlag = 0
        sweepFlag    = 1
        
        svgCode = "\n<circle cx=\""+str(cx)+"\" cy=\""+str(cy)+"\" r=\""+str(outerCircleRadius)+"\" fill=\""+outerFillColour+"\" stroke=\""+outerStrokeColour+"\" stroke-width=\""+str(outerStrokeWidth)+"\" />\n"
        svgCode = svgCode + "<circle cx=\""+str(cx)+"\" cy=\""+str(cy)+"\" r=\""+str(innerCircleRadius)+"\" fill=\""+innerFillColour+"\" stroke=\""+innerStrokeColour+"\" stroke-width=\""+str(innerStrokeWidth)+"\" />\n"
        svgCode = svgCode + "<path\n"
        svgCode = svgCode + "\td=\"M "+str(X1)+","+str(Y1)+"\n"
        svgCode = svgCode + "\tL "+str(X2)+","+str(Y2)+"\n"
        #svgCode = svgCode + "\tL "+str(X3)+","+str(Y3)+"\n"
        svgCode = svgCode + "\tA "+ str(dataCircleRadius) + "," + str(dataCircleRadius) + " 0 "+str(largeArcFlag)+","+str(sweepFlag)+" "+ str(X3)+","+str(Y3)+"\n"
        svgCode = svgCode + "\tZ\"\n"
        svgCode = svgCode + "fill=\""+dataFillColour+"\" stroke=\""+dataStrokeColour+"\" stroke-width=\""+str(dataStrokeWidth)+"\" id=\"circleChart-"+pathID+"\" />"
        
        self.inputSVG = insertFreeformSvgCode( self.inputSVG, svgCode )
        
        #style="opacity:1;fill:#ff0000;fill-opacity:1;stroke:#000000;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
        
            
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
    
    
    