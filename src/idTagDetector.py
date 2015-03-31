# takes a string as input. Detects SVG tags susceptible of designating geographical divisions
# such as continents, countries, administrative subdivitions, etc.

#from bs4 import BeautifulSoup
import re

    
class IdTagDetector:
    def __init__(self, arg):
        self.arg=arg
        self.detectedTags=[]
        
        self.stoplist=[]
        self.stoplistPath="../configs/stoplists"
        self.whitelist=[]        
        self.whitelistPath="../configs/whitelists"        
        # The prefixes that have been observed to hold geographic labels in the test maps 
        self.labelPrefixes = ["path class=", "inkscape:label=", "label=", "id="]
        
    #
    def loadStopList(self):
        return []
    
    #
    def loadWhiteList(self):
        return []
    

    #
    def listTags(self):
        print(self.detectedTags)
        
    #
    def detect(self):
        candidates = []
        for labelPrefix in self.labelPrefixes:
            regex = labelPrefix+"\"([^0-9]+?)\""
            candidates.extend( re.findall(regex, self.arg) )
            
        self.detectedTags = candidates
        
        
        
        
        #subdivisionTag = "path"
        #labelTag       = "inkscape:label"
        
        #soup = BeautifulSoup(self.arg)
        #candidates = soup.findAll(subdivisionTag)
        #for candidate in candidates:
            #print(candidate)
            ##if candidate[labelTag][0] == "#":
                ##break     
            ##if candidate.has_attr(labelTag):
                ##self.detectedTags.append(candidate[labelTag])            
            ##self.detectedTags.append(candidate[labelTag])

#####################################################################        
#####################################################################
###############################################
#../maps/Blank_Map_Africa_1932.svg     
#<path class="land tn" d="m 1329,465 c 0 (...),-4" id="path5410"></path>
# ==> tn
###############################################
#../maps/USA_Counties_with_FIPS_and_names.svg
#<path d="M 155.88098,77.694 (...) L 155.54698,80.155 L 155.88098,77.694" id="56039" inkscape:label="Teton, WY" style="font-size:12px;fill:#d0d0d0;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel"></path>
# ==> Teton, WY
###############################################
#../maps/Blank_map_of_Europe_1815.svg
#<path d="m 6315.6975,5206.8332 (...)-1.9098 z" id="Serbia" style="fill:#c0c0c0;stroke:#ffffff;stroke-width:6.11153841;stroke-miterlimit:4;stroke-dasharray:6.11153881, 12.22307732;stroke-dashoffset:0"></path>
# ==> Serbia
###############################################
#../maps/World98.svg
#<g id="Iran:Semnan Province">
        #<path d='M5242.6766527
#1029.3724017z' fill='white' stroke='black' />
#</g>
 #==> Iran:Semnan Province

#####################################################################
# path class="land tn"
# inkscape:label="Teton, WY"
# id="Serbia"
# <g id="Iran:Semnan Province">







