from math import radians, sin, cos, asin, sqrt
import xlrd
import xml.etree.cElementTree as ET

# TODO: Add exception handling
# TODO: Add constants to top
# TODO: Change into Class

# function to convert given coord from COIN format to +/- decimal degrees
def coordConverter( coord):
    # strip leading spaces
    coord = coord.lstrip(" ")
    # remove degree symbol "\xb0"
    coord = coord.encode("ascii", "ignore")
    coord = coord.replace(" ", "'")
    # split into degree [0] / minute [1] / sign [2]
    coord = coord.split("'")
    degree = int(coord[0].replace("-", ""))
    minute = float(coord[1])
    sign = 1
    # check if given coordinate is negative
    if coord[2] == 'S' or coord[2] == 'W':
        sign = -1
    coord = (sign * (degree + (minute / 60)))
    return coord

# function that returns great circle distance between two
# points on the earth (input must be in decimal degrees)
def haversine(lat1, long1, lat2, long2):
    # in meters
    earthRadius = 6378100
    
    # convert decimal degrees to radians 
    lat1 = radians(lat1)
    long1 = radians(long1)
    lat2 = radians(lat2)
    long2 = radians(long2)

    # haversine formula 
    dlong = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c = 2 * asin(sqrt(a)) 

    m = earthRadius * c
    return m 

# function to print target list with attributes to console 
# for debugging
def printTargets( targetList):
    # print targets
    for target in targetList:
        for attribute in target:
            print attribute, 
        print "\n"
        #break

# function that takes report file name, opens COIN PMD report
# and returns list containing target data with attributes
def coinContactFormatter( reportName):
    extension = ".xlsx"
    
    filename = reportName + extension
    # open workbook
    book = xlrd.open_workbook(filename, on_demand=True)
    # open sheet
    # ASSUMPTION: There is only one sheet (position 0)
    sh = book.sheet_by_index(0) 
    # list to hold targets
    targets = []
    
    # Find rows containing targets
    # ASSUMPTION: Target row always starts with "CRN: " in column 1
    # ASSUMPTION: Target category is always current "CRN: " row + 2 in column 2
    # ASSUMPTION: Target coordinates are always in current "CRN: " row + 5 in column 2
    for row in range(sh.nrows):
        # list to hold target information
        target = []
        # check if valid row and target row
        if sh.cell_value(rowx=row, colx=1) and sh.cell_value(rowx=row, colx=1).startswith("CRN: "):
            # strip off "CRN: " prefix add mission name
            target.append(reportName)
            targetName = sh.cell_value(rowx=row, colx=1)
            targetName = targetName.split(" ")
            # add name to target attribute list
            target.append(targetName[1])
            # grab target type from current row
            targetType = sh.cell_value(rowx=row+2, colx=2)
            targetType = targetType.split(" ")
            # add type to target attribute list
            target.append(targetType[1])
            # grab target coord from current row
            targetCoord = sh.cell_value(rowx=row+5, colx=2)
            # split coord into LAT and LONG
            targetCoord = targetCoord.split(",")
            # lat first then long
            targetLat = targetCoord[0].split(" ")
            targetCoord[0] = targetLat[1] + " " + targetLat[2]
            targetLat = coordConverter(targetCoord[0])
            # add target LAT to target attribute list
            target.append(targetLat)
            targetLong = coordConverter(targetCoord[1])
            # add target LONG to target attribute list
            target.append(targetLong)
            # add target to list of targets
            targets.append(target)

    # duplicate check
    temp = []
    for target in targets:
        if target not in temp:
            temp.append(target)
             
    targets = temp
    return targets
            
# function for comparing two COIN PMD missions and
# writing output to csv file
# TODO: extend to any number of missions (list of target lists as input)
def contactLocalization( missionOne, missionTwo, maxDist, outputName):
    # extension of output file, CSV
    outputName = outputName + ".csv"
    # create / open output file in write mode
    fout = open(outputName, 'w')
    
    # Print contact matches to ground truth position within maxDist
    fout.write("Ground truth calls within distance of " + str(maxDist) + "m\n")
    fout.write("Source, Name, Category, LAT, LONG, Distance\n")
    for a in missionOne:
        for b in missionTwo:
            if haversine(a[3], a[4], b[3], b[4]) < maxDist:
                fout.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "," + str(a[4]) + "," + str(haversine(a[3], a[4], b[3], b[4])) + "\n")
                fout.write(str(b[0]) + "," + str(b[1]) + "," + str(b[2]) + "," + str(b[3]) + "," + str(b[4]) + "\n")
                fout.write(",\n")
    
    # Print false alarms 
    fout.write("False alarms\n")
    fout.write("Source, Name, Category, LAT, LONG\n")
    for a in missionTwo:
        present = False
        for b in missionOne:
            if haversine(a[3], a[4], b[3], b[4]) < maxDist:
                present = True
        if present == False:
            fout.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "," + str(a[4]) + "\n")
    fout.write("\n")     
    
    fout.close()
    
# function for parsing contact XML file
def contactParser( fileName):
    # extension of input file, XML
    fileName = fileName + ".XML"
    
    message = ET.ElementTree(file=fileName)
    
    for contact in message.iter(tag='{http://www.saic.com/navy/miwml.1.0}TacticalContact'):
       
        for attribute in contact.iter():
            
            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}TacticalContact':
                print attribute.attrib['contact_id']
                
            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}CRN':
                print attribute.text
                
            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}Latitude':
                #TODO: Add attribute units check
                print attribute.text

            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}Longitude':
                #TODO: Add attribute units check
                print attribute.text
                
            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}ContactKind':
                print attribute.text

            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}CaseDepth':
                print attribute.text + ' ' + attribute.attrib['units']

    
#     # Open the file 
#     f = open(fileName, 'r')
#     # Read line 1
#     line = f.readline()
#     while line:
#         parts = line.split()
#         # check for contact tag
#         if parts[0] == "<TacticalContact":
#             print parts[0]
#             line = f.readline()
#             # check for CRN
#             print line
#         line = f.readline()
# #    while line:
# #        print line
# #        line = file.readline()
#         
#     # Close the file
#     f.close()