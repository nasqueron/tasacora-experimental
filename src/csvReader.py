import csv

SVG_NS = "http://www.w3.org/2000/svg"



#---------------------------------------------------------
# Detects wheter data seems to be of Boolean type
def allDataBoolean(data):
    for i in data:
        if not ( i == 0 or i == 1 ):
            return False
    return True

# Detects wheter data seems to be of Integer type
def allDataInteger(data):
    for i in data:
        if not isinstance(item, int):
            return False
    return True

# Detects wheter data seems to be of Percentage type
def allDataPercentage(data):
    for i in data:
        if ( 1<0 or i>100 ):
            return False
    return True
#---------------------------------------------------------
    
# Read a CSV file, returns a dict. Useful to populate self.data of a csvDataReader
def readFile(inFile):
    data = {}
    with open(inFile, 'rt') as f:
        for line in f:
            line = line.rstrip('\n')
            key   = ( line.split("\t") )[0]
            value = ( line.split("\t") )[1]
            data[key] = value
    return data
    
#---------------------------------------------------------

#=========================================
# Class to handle CSV data
class csvReader:

    def __init__(self, arg):
        self.infile = arg
        self.data   = readFile(self.infile)
        
    def getLabels(self):
        return self.data.keys()

    def prettyPrint(self):
        line = "Data of file \""+ self.infile +"\":"
        horizontalBar = "+"+"-"*(len(line) + 2)+"+"
        print (horizontalBar)
        print ("| "+line+" |")
        print (horizontalBar)
        for i in self.data.keys():
            print( "\t",i,"\t",self.data[i])
        print (horizontalBar+"\n")
    
    # Detects if the numerical data is Boolean, Intergers, Percentages or just plain Reals.
    def detectDataType(self):
        dataToTest = self.data.values()
        if( allDataBoolean( dataToTest )    ):
            return "bool"
        if( allDataInteger( dataToTest )    ):
            return "int"
        if( allDataPercentage( dataToTest ) ):
            return "percent"
        return "real"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    