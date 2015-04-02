# takes an SVG file as input. Creates a table associating geographic identifiers and their colours.
# Writes an SVG file with new colours.

#from bs4 import BeautifulSoup
#import re


class SvgColourManager:
    # Just used in constructor to fill self.listOfIDs
    def fillListOfIDs(self):
        from idTagDetector import IdTagDetector
        detector = IdTagDetector(self.inputSVG)
        detector.detect()
        return detector.detectedTags    
    
    def __init__(self, arg):
        #self.inputSVG       = open(arg, 'r').read()
        self.inputSVG       = arg
        self.tagsAndColours = {}
        self.listOfIDs      = self.fillListOfIDs()


        
    # sets all subdivision in white
    def colourAllWhite(self):
        for area in self.listOfIDs:
            self.tagsAndColours[area] = "#FFFFFF"

    # I see a red door and I want to paint it blaaaack. 
    # Sorry.
    # sets all subdivision in black
    def colourAllBlack(self):
        for area in self.listOfIDs:
            self.tagsAndColours[area] = "#000000"

    # sets all subdivision in white
    def colourAllRandom(self):
        import random
        for area in self.listOfIDs:
            self.tagsAndColours[area] = hex(random.randint(0, 16777215))[2:].upper()    
    

    # Outputs content of self.tagsAndColours to standard output.
    def listTagsAndColours(self):
        for tag in self.tagsAndColours.keys():
            print(tag+"\t\t"+self.tagsAndColours[tag])


    def editMap(self):
        import re
        
        regex = re.compile("(<\?xml.*?>\s*\n*\s*<svg.*?>)", re.DOTALL)

        print( (re.split (regex, self.inputSVG))[1] )
        print()
        # ----------------------------------------------
        print("<style type=\"text/css\"><![CDATA[")
        for tag in self.tagsAndColours.keys():
            print("\t#"+tag+" { fill: #"+self.tagsAndColours[tag]+" }")
        print("]]></style>")
        # ----------------------------------------------
        print()
        print( (re.split (regex, self.inputSVG))[2] )


        
        
        
        
        
        