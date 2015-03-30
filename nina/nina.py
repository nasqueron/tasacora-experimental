#!/usr/bin/python
import argparse
import csv
import sys
from bs4 import BeautifulSoup


#-----------------------------------
# Management of arguments
parser = argparse.ArgumentParser(description='Colours counties in SVG map depending on data.')
parser.add_argument('-i', '--infile', dest='infile', action='store',
                   default="data.txt",
                   help='set input from statistical data file (default: \"data.txt\")')
parser.add_argument('-m', '--map', dest='mapfile', action='store',
                   default="map.svg",
                   help='set SVG file to be coloured (default: \"map.svg\")')
parser.add_argument('-o', '--output', dest='outfile', action='store',
                   default="output.svg",
                   help='set output file (default: \"output.svg\")')

args = parser.parse_args()
#-----------------------------------
# Loads data from data file
# (Specific to "FATAL ENCOUNTERS SPREADSHEET (Responses) - Form Responses.csv")
def loadDataFromFile(infile):
    dataBySubdivision = {}
    dataLine = csv.reader(open(infile), delimiter=",")
    next(dataLine) # skip headers
    for row in dataLine:
        victimName            = row[1].strip()
        victimAge             = row[2].strip()
        victimGender          = row[3].strip()
        victimSoCalledRace    = row[4].strip()
        victimPhoto           = row[5].strip()
        incidentDate          = row[6].strip()
        incidentAddress       = row[7].strip()
        incidentCity          = row[8].strip()
        incidentState         = row[9].strip()
        incidentZipCode       = row[10].strip()
        incidentCounty        = row[11].strip()
        incidentResponsible   = row[12].strip()
        causeOfDeath          = row[13].strip()
        circumstances         = row[14].strip()
        justifiedOrNot        = row[15].strip()
        newsArticle           = row[16].strip()
        psychiatricEvaluation = row[17].strip()
        source                = row[18].strip()
        emailAddress          = row[19].strip()
        date                  = row[20].strip()
        #nothing at position 21        
        IncidentIdentifier    = row[22].strip()  
        
        subdivision = incidentCounty+", "+incidentState
        if(subdivision in dataBySubdivision.keys()):
            dataBySubdivision[subdivision] = dataBySubdivision[subdivision]+1
        else:
            dataBySubdivision[subdivision] = 1
    return dataBySubdivision

#-----------------------------------
# Levensthein distance between two strings
def levenshtein(arg1, arg2):
    #trivial cases
    if arg1 == arg2: return 0
    if arg1 == ''  : return len(arg2)
    if arg2 == ''  : return len(arg1)
    #
    distance = 666 # If "666" is returned, you probably have a problem.
    v1 = [i for i in range (0, len(arg2))]
    v2 = [i for i in range (0, len(arg2))] 
    for i in range (0, len(arg1)):
        v2[0] = i + 1
        for j in range (1, len(arg2)):
            cost = 0
            if not arg1[i] == arg2[j]:
                cost = 1
            v2[j] = min(v2[j-1]+1, v1[j], v1[j-1]+cost)
        for j in range (0, len(v1)):
            v1[j] = v2[j]
    distance = v2[len(arg2)-1]-1
    # Uncomment this line if you want to see the values (debug)
    #print "Dist \""+arg1+\"" - \""+arg2+"\": "+str(distance)	
    return distance

# Returns the element of argList that has the smallest distance to argString
def levenshtein_all(argString, argList):
    #trivial case
    if(argString in argList):
        return argString
    #non-trivial
    bestDistance  = 999999
    bestCandidate = ""
    for argListElement in argList:
        thisDistance  = levenshtein(argListElement, argString)
        if thisDistance < bestDistance: 
            bestDistance  = thisDistance
            bestCandidate = argListElement
    return bestCandidate

#-----------------------------------
# Creates a dictionary of subdivision identifiers
#   keys: subdivisions per Data file conventions (as found in dataBySubdivision)
#   values: subdivision identifiers as present in the map (SVG) file.
def fillSubdivisionDict(dataDict, svgMapFile):
    subdivisionLabelCorrespondanceDict = {}
    subdivisionLabelsInSVG  = []
    subdivisionLabelsInData = dataDict.keys()
    
    # Filling subdivisionLabelsInSVG
    svg = open(svgMapFile, 'r').read()
    subdivisionTag = "path"
    labelTag       = "inkscape:label"
    soup = BeautifulSoup(svg)
    #soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])
    subdivisions = soup.findAll(subdivisionTag)
    for subdivision in subdivisions:
        if subdivision.has_attr(labelTag):
            subdivisionLabelsInSVG.append(subdivision[labelTag])

    # Detect mismatchs and attempt to find correspondances.
    mismatchingLabelsDict = {}
    counter = 0
    for subdivisionLabelInData in subdivisionLabelsInData:
        sys.stdout.write("\rChecking data consistancy:  %d / %d" % (counter,len(subdivisionLabelsInData)) )
        sys.stdout.flush()
        #print("\r"+str(counter) + "/" + str(len(subdivisionLabelsInData)))
        counter = counter + 1
        correspondingLabel = levenshtein_all(subdivisionLabelInData, subdivisionLabelsInSVG)
        subdivisionLabelCorrespondanceDict[subdivisionLabelInData] = correspondingLabel
        #subdivisionLabelsInSVG.remove(correspondingLabel)
        if not (subdivisionLabelInData == correspondingLabel):
            #print ( subdivisionLabelInData+" --> "+correspondingLabel )
            mismatchingLabelsDict[subdivisionLabelInData] = correspondingLabel
    print()

    if (len(mismatchingLabelsDict) > 0):
        print("  *** CAUTION: the following names do not match in Data file and Map file and")
        print("               will automatically be made to match. Please check for errors."  )
        print("               If necessay, correct the labels in the data file and re-run."  )
        print(""  )
        print("               Name in Data --> Name in Map."  )
        print("               -----------------------------"  )
        for i in mismatchingLabelsDict:
            print("               "+i+" --> "+mismatchingLabelsDict[i])
            #if not (i == subdivisionLabelCorrespondanceDict[i]):
                #print ( i+" --> "+subdivisionLabelCorrespondanceDict[i] )

    return subdivisionLabelCorrespondanceDict  
#-----------------------------------
# Precomputes hexadecimal colour values to put into SVG
def computeColours(dataBySubdivision, subdivisionIndentifierCorrespondance):
    colourBySubdivision = {}
    maximumValue = max(dataBySubdivision.values())
    
    import math
    for i in dataBySubdivision:
        greenValue = (maximumValue - dataBySubdivision[i])/maximumValue*255
        #redValue   = dataBySubdivision[i]/maximumValue*255
        redValue   = math.log(dataBySubdivision[i])/math.log(maximumValue)*255
        blueValue  = 0
        #rgbTuple   = (greenValue, redValue, blueValue)
        rgbTuple   = (greenValue, greenValue, greenValue)
        hexColour  = '#%02x%02x%02x' % rgbTuple
        #hexColour  = "#FFFF00"
        colourBySubdivision[subdivisionIndentifierCorrespondance[i]]=hexColour
    
    return colourBySubdivision

 #-----------------------------------
 # puts desired colours into SVG file.
def editMap(svgMapFile, colourBySubdivision):
    
    svg = open(svgMapFile, 'r').read()
    subdivisionTag = "path"
    labelTag       = "inkscape:label"
    soup = BeautifulSoup(svg)
    subdivisions = soup.findAll(subdivisionTag)
    
    #pathStyle = "font-size:12px;fill:#d0d0d0;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel"
    pathStylePrefix  = "font-size:12px;fill:"
    pathStylePostfix = ";fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel"
    
    #print(colourBySubdivision.keys())
    for subdivision in subdivisions:
        #print (subdivision['id'], subdivision['inkscape:label'])
        if (subdivision['id'] not in ["State_Lines", "separator"]) :
            if (subdivision['inkscape:label'] in colourBySubdivision.keys()):
                subdivisionColour = colourBySubdivision[subdivision['inkscape:label']]
                #print("   known subdivision: "+subdivision['inkscape:label']+", colour = "+subdivisionColour)
            else:
                subdivisionColour = "#FFFFFF"
                #print("   *** CAUTION: unknown subdivision: "+subdivision['inkscape:label'])
            subdivision['style'] = pathStylePrefix + subdivisionColour + pathStylePostfix
    #print(sorted(colourBySubdivision.keys()))
    # Output map
    return soup.prettify()

#-----------------------------------
def saveMap(svgContent, outfile):
    print("Saving results to "+outfile+"..."),
    f = open(outfile,'w')
    f.write(svgContent) # python will convert \n to os.linesep
    f.close() # you can omit in most cases as the destructor will call if
    print("   DONE.")
###################################################################
#-----------------------------------
print("Reading statistical data from "+args.infile+" and geographic data from "+args.mapfile+". Outputing results to "+args.outfile+".")

dataBySubdivision = {}
dataBySubdivision = loadDataFromFile(args.infile)

subdivisionIndentifierCorrespondance = {}   # translates the identifiers of subdivisions from Data file conventions to SVG map conventions.
subdivisionIndentifierCorrespondance = fillSubdivisionDict(dataBySubdivision, args.mapfile)

colourBySvgSubdivision = computeColours(dataBySubdivision, subdivisionIndentifierCorrespondance)
svgContent = editMap(args.mapfile, colourBySvgSubdivision)
saveMap(svgContent, args.outfile)


print("I rest my case")





