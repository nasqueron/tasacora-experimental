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
            self.tagsAndColours[area] = "#"+hex(random.randint(0, 16777215))[2:].upper()    

    # sets all subdivision in white
    def colourAllRandomRed(self):
        import random
        for area in self.listOfIDs:
            #self.tagsAndColours[area] = hex(random.randint(0, 16777215))[2:].upper()  
            redValue  = random.randint(100, 255)
            rgbTuple  = (255, 255-redValue, 255-redValue)
            hexColour = '%02x%02x%02x' % rgbTuple
            self.tagsAndColours[area] = "#"+hexColour

    # Outputs content of self.tagsAndColours to standard output.
    def listTagsAndColours(self):
        for tag in self.tagsAndColours.keys():
            print(tag+"\t\t"+self.tagsAndColours[tag])

    # blanks (sets "fill=None") the elements in the list. Useful for borders etc.
    def blankElementsInList(self, arg):
        for i in arg:
            if i in self.tagsAndColours.keys():
                self.tagsAndColours[i] = "none"

    # Inserts CSS style instructions between header and body of the SVG file.
    def editMap(self):
        import re
        
        #Assembles output line, inserting CSS style instructions between header and body of the SVG file.
        regex = re.compile("(^.*?<svg.*?>)(.*)", re.DOTALL)
        m = regex.match(self.inputSVG)
        splitFile = re.split (regex, self.inputSVG)
        outputString = m.group(1) + "\n"
        outputString = outputString+"<style type=\"text/css\"><![CDATA[\n"
        for tag in self.tagsAndColours.keys():
            outputString = outputString+"\t#"+tag+" { fill: "+self.tagsAndColours[tag]+" }\n"
        outputString = outputString+"]]></style>\n"+m.group(2)
        
        print(outputString)
        
        
        

        
        
        
        
        
        