#import xml.etree.cElementTree as ET
from lxml import etree
import re
from math import *

SVG_NS = "http://www.w3.org/2000/svg"



# Class to hanle XML trees in SVG files.
class SvgTreeManager:
    def __init__(self, arg):
        self.svg = arg.encode('utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        self.tree = etree.fromstring(self.svg, parser=parser)
        
    # ----------------------------------------
    # returns a list of SVG Paths with that name
    def findPath(self, name=""):
        work = []
        for node in self.tree.findall('.//{%s}path' % SVG_NS):
            if (name in node.get('id')):
                work.append(node)
        return work
    
    # ----------------------------------------
    # returns parent node of current XML node
    def findParent(self, node):
        return node.find("..")
    
    # ----------------------------------------
    # returns a list of parent nodes of current XML node in ascending order (root will bit last in the list)
    def findParents(self, node):
        currentNode = node
        ancestry    = []
        while True:
            currentNode = self.findParent(currentNode)
            if currentNode is None:
                break
            else:
                ancestry.append(currentNode)
        return ancestry
    
    # ----------------------------------------
    # returns transformation (as in 
    #      transform="matrix(15.278846,0,0,15.278846,3144.1413,1135.7902)"
    # notation)
    def getTransform(self, node):
        return node.get('transform')
    
    # ----------------------------------------
    # returns local transformation matrix (tranf. mat. defined in the element itself)
    def getTransformMatrix(self, node):
        return toMatrix( self.getTransform(node) )
    
    # ----------------------------------------
    # returns overall tranformation matrix of parent node (even if nested)
    def getParentsTransformMatrix(self, node):
        matrices = []
        for j in self.findParents(node):
            n = toMatrix( self.getTransform(j) )
            matrices.append(n)
        matrices.reverse()
        m = [1,0,0,1,0,0]
        for j in matrices:
            m = multiplySvgMatrices (m, j)   
        return m
    
        #m = [1,0,0,1,0,0]
        #for j in self.findParents(node):
            #n = toMatrix( self.getTransform(j) )
            ##m = multiplySvgMatrices (n, m)
            #m = multiplySvgMatrices (m, n)            
        #return m
    
    # ----------------------------------------
    # returns total transformation matrix, applying parent transformations (even if nested).
    def getTotalTransformMatrix(self, node):
        a = self.getParentsTransformMatrix(node)
        b = self.getTransformMatrix(node)
        #return multiplySvgMatrices(b, a)
        return multiplySvgMatrices(a, b)
        #return [1,0,0,1,0,0]
    
    # ----------------------------------------    
    # computes the barycentre of the points of a path.
    def centreOfMass(self, path):
    
        coordinatesX = (self.extractPoints(path))[0]
        coordinatesY = (self.extractPoints(path))[1]
                    
        #barycentreX = sum(coordinatesX)/len(coordinatesX) # + offsetX
        #barycentreY = sum(coordinatesY)/len(coordinatesY) # + offsetY
        #barycentreX = ( max(coordinatesX) - min(coordinatesX) )/2.0 + min(coordinatesX) # + offsetX
        #barycentreY = ( max(coordinatesY) - min(coordinatesY) )/2.0 + min(coordinatesY) # + offsetY 
        barycentreX = median(coordinatesX)
        barycentreY = median(coordinatesY)
        #................................
        barycentre  = [barycentreX, barycentreY]
        return barycentre
    
    
    # ----------------------------------------
    # Extracts significant points from a path, applying transforms for Translation and Matrix (removes control points from path).
    def extractPoints(self, path):
        from itertools import islice
        import re
        
        # This will extract the endpoints of the segments forming the path (removing control points)
        coordinatesX = []
        coordinatesY = []
        offsetX      = 0.0 
        offsetY      = 0.0
        pathData      = path.get('d')
        #transformData = path.get('transform')
        pathData = re.findall('[a-df-zA-DF-Z]+|[\\d.eE\-]+', pathData) # To separate lettres from numbers. E is special case (exponent)
        path_iter = iter( pathData )
        
        #................................
        state         = "start"
        typeOfSegment = "" # can take values MLHVCSQTAZmlhvcsqtaz
        previousX = 0.0
        previousY = 0.0
        for i in path_iter:
            i = i.replace(',', '')
            if (state == "start"):

                if (typeOfSegment in "MLHVCSQTAZ"): # Absolute coordinates
                    previousX = 0.0
                    previousY = 0.0       

                if (i in "Zz"): # We have encountered a STOP signal. Exit loop.
                    break
                
                if (i in "MLHVCSQTAmlhvcsqta"): # We have encountered a new segment-type. Set typeOfSegment accordingly.
                    typeOfSegment = i
                    continue

                # Setting states to perform operations
                if (typeOfSegment in "MmLlHhVvTt"):
                    state = "recieveX" 
                if (typeOfSegment in "SsQq"):
                    state = "wait2"
                if (typeOfSegment in "Cc"):
                    state = "wait4"       
                if (typeOfSegment in "Aa"):
                    state = "wait5"    
                #if (typeOfSegment in "Zz"):
                    #break
                
            if (state == "recieveX"):
                newX = float(i) + previousX
                coordinatesX.append( newX )
                previousX = newX
                state = "recieveY"
                continue
            if (state == "recieveY"):
                newY = float(i) + previousY
                coordinatesY.append( newY )
                previousY = newY
                state = "start"  
                continue
            if (state == "wait5"):
                next(islice(path_iter, 3, 4), '')
                state = "recieveX"
                continue
            if (state == "wait4"):
                next(islice(path_iter, 2, 3), '')
                state = "recieveX"
                continue
            if  (state == "wait2"):
                next(islice(path_iter, 0, 1), '')            
                state = "recieveX"
                continue
        
        #................................
        #if (transformData):
            #newCoordinatesX = []
            #newCoordinatesY = []
            #transformDataValues = re.findall(r"[-+]?\d*\.\d+|\d+", transformData)
            #if "translate" in transformData:
                #for coordinateX, coordinateY in zip(coordinatesX, coordinatesY):
                    #newCoordinatesX.append( coordinateX + float(transformDataValues[0]) )
                    #newCoordinatesY.append( coordinateY + float(transformDataValues[1]) )
            #if "matrix" in transformData:
                #for coordinateX, coordinateY in zip(coordinatesX, coordinatesY):
                    #newCoordinatesX.append( float(transformDataValues[0])*coordinateX + float(transformDataValues[2])*coordinateY + float(transformDataValues[4]) )
                    #newCoordinatesY.append( float(transformDataValues[1])*coordinateX + float(transformDataValues[3])*coordinateY + float(transformDataValues[5]) )
            #coordinatesX = newCoordinatesX
            #coordinatesY = newCoordinatesY    
            
        M = self.getTotalTransformMatrix(path)
        
        newCoordinatesX = []
        newCoordinatesY = []        
        for coordinateX, coordinateY in zip(coordinatesX, coordinatesY):
            v = [coordinateX, coordinateY]
            v = multiplySvgMatrixVector(M, v)
            newCoordinatesX.append( v[0] )
            newCoordinatesY.append( v[1] )
        
        return [newCoordinatesX, newCoordinatesY]
        #return [coordinatesX, coordinatesY]
        
    
#===============================        
# Stand-alone functions
#
# This is a procedural marxist utopia:
# classless subroutines.
#===============================        
        
# ---------------------
# detects if a string is a float
def isFloat(str):
    try:
        float(str)
    except ValueError:
        return False 
    return True

# matrice-vector multiplication
# matrix = [a,b,c,d,e,f]
# vector = [x, y]
def multiplySvgMatrixVector(M,V):
    a = M[0]
    b = M[1]
    c = M[2]
    d = M[3]
    e = M[4]
    f = M[5]    
    
    x = V[0]
    y = V[1]
    
    x_out = a*x + c*y + e
    y_out = b*x + d*y + f
    
    return [x_out, y_out]


#transform="matrix(a,b,c,d,e,f)"
def multiplySvgMatrices(M1,M2):
    a1 = M1[0]
    b1 = M1[1]
    c1 = M1[2]
    d1 = M1[3]
    e1 = M1[4]
    f1 = M1[5]
    
    a2 = M2[0] 
    b2 = M2[1] 
    c2 = M2[2] 
    d2 = M2[3] 
    e2 = M2[4] 
    f2 = M2[5] 
    
    a3 = a1*a2 + c1*b2
    b3 = b1*a2 + d1*b2
    c3 = a1*c2 + c2*d2
    d3 = b1*c2 + d1*d2
    e3 = a1*e2 + c1*f2 + e1
    f3 = b1*e2 + d1*f2 + f1
    
    return [a3, b3, c3, d3, e3, f3]

#transform="matrix(a,b,c,d,e,f)"
def addSvgMatrices(M1,M2):
    a1 = M1[0]
    b1 = M1[1]
    c1 = M1[2]
    d1 = M1[3]
    e1 = M1[4]
    f1 = M1[5]
    
    a2 = M2[0] 
    b2 = M2[1] 
    c2 = M2[2] 
    d2 = M2[3] 
    e2 = M2[4] 
    f2 = M2[5] 
    
    a3 = a1 + a2 
    b3 = b1 + b2 
    c3 = c1 + c2 
    d3 = d1 + d2 
    e3 = e1 + e2 
    f3 = f1 + f2 
    
    return [a3, b3, c3, d3, e3, f3]


# ----------------------------------------
# Converts SVG code describing transformations into 6-element matrices
def toMatrix(string):
    work = [1, 0, 0, 1, 0, 0] # identity in this algebra
    
    # cf http://commons.oreilly.com/wiki/index.php/SVG_Essentials/Matrix_Algebra
    # Matrix (3x3, only 6 variable componants):
    # ( a c e )
    # ( b d f )
    # ( 0 0 1 )
    
    # useful testing tool: https://petercollingridge.appspot.com/svg-transforms
    
    if string is None:
        return work
    
    regex  = re.compile('[\),\(, ,]')
    string = list ( filter( None, re.split(regex, string) ) )
    #print (string)
    
    state=""
    items = iter(string)
    for item in items:
        #a = b = c = d = e = f = 0
        
        # State machine
        if ("translate" in item):
            state = "translate"
        if ("rotate" in item   ):
            state = "rotate"
        if ("scale" in item    ):
            state = "scale"
        if ("skewX" in item    ):
            state = "skewX"
        if ("skewY" in item    ):
            state = "skewY"        
        if ("matrix" in item   ):
            state = "matrix"
            
        # Translation: two attributes
        if (state == "translate"):
            e = float( next(items) )
            f = float( next(items) )
            work = multiplySvgMatrices ( work, [1, 0, 0 , 1, e , f])
            #work = multiplySvgMatrices ( [1, 0, 0 , 1, e , f], work )

        # Rotation: one or three attributes    
        # transform="rotate(15)"         --> rotation of 15 degrees clockwise around (0,0)
        # transform="rotate(15, 40, 40)" --> rotation of 15 degrees clockwise around (40,40) 
        if (state == "rotate"):
            angle = radians( float( next(items) ) ) 
            try:
                x     = next(items)
            except StopIteration:
                work  = multiplySvgMatrices ( work, [cos(angle), sin(angle),-sin(angle),cos(angle),0,0] )                
                #work  = multiplySvgMatrices ( [cos(angle), sin(angle),-sin(angle),cos(angle),0,0], work )
                break
            if not isFloat(x):
                work  = multiplySvgMatrices ( work, [cos(angle), sin(angle),-sin(angle),cos(angle),0,0] )
                #work  = multiplySvgMatrices ( [cos(angle), sin(angle),-sin(angle),cos(angle),0,0], work )
                state = x
            else:
                x = float( x )
                y = float( next(items) )
                e = -x*cos(angle) + y*sin(angle) + x
                f = -x*sin(angle) - y*cos(angle) + y
                work  = multiplySvgMatrices ( work, [cos(angle), sin(angle),-sin(angle),cos(angle), e, f] )
                #work  = multiplySvgMatrices ( [cos(angle), sin(angle),-sin(angle),cos(angle), e, f], work )

        # Scale: one or two arguments
        #transform="scale(2)"            --> Homotethy factor 2 (multiplies coordinates, heigth and width
        #transform="scale(2,3)"          --> Homotethy factor 2 on X axis and 3 on Y axis
        if (state == "scale"):
            a = float( next(items) )
            try:
                b = next(items)
            except StopIteration:
                work = multiplySvgMatrices ( work, [ a, 0, 0, a, 0, 0 ] )
                #work = multiplySvgMatrices ( [ a, 0, 0, a, 0, 0 ], work )
                break
            if not isFloat(b):
                work = multiplySvgMatrices ( work, [ a, 0, 0, a, 0, 0 ] )
                #work = multiplySvgMatrices ( [ a, 0, 0, a, 0, 0 ], work )
                state = b
            else:
                b = float ( b )
                work = multiplySvgMatrices ( work, [ a, 0, 0, b, 0, 0 ] )
                #work = multiplySvgMatrices ( [ a, 0, 0, b, 0, 0 ], work )
            
        # Skew: one attribute. Exists in "SkewX" and in "SkewY" flavours.
        if (state == "skewX"):
            a = radians( float( next(items) ) )
            work = multiplySvgMatrices ( work, [1, 0, tan(a), 1, 0 , 0] )
            #work = multiplySvgMatrices ( [1, 0, tan(a), 1, 0 , 0], work )
        if (state == "skewY"):
            a = radians( float( next(items) ) )
            work = multiplySvgMatrices ( work, [1, tan(a), 0 , 1, 0 , 0] )
            #work = multiplySvgMatrices ( [1, tan(a), 0 , 1, 0 , 0], work )
        
        # General matrix: only six attributes
        # NB: in case you were wondering: this allows parsing lines such as
        #     transform "translate(-1539.5729,-974.79019) matrix(1, 3.14, 23, 6, 0.7462, 42) rotate(50, -1000, 314) scale(2, 3)"
        # It should not happen in an sane environment, but we want to be belt-and-braces.
        if (state == "matrix"):
            a = float( next(items) )
            b = float( next(items) )
            c = float( next(items) )
            d = float( next(items) )
            e = float( next(items) )
            f = float( next(items) )
            work = multiplySvgMatrices ( work, [a, b, c, d, e, f] )
            #work = multiplySvgMatrices ( [a, b, c, d, e, f], work )

    return work
    
#--------------------------
# median
def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    #if not length % 2:
        #return (sorts[int(length / 2)] + sorts[int(length / 2 - 1)]) / 2.0
    indice = int(length / 2)
    return sorts[int(length / 2)]
        

        
    
    
    
    
    
    
    
    
    
    
    
    