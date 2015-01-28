import math
import xlrd

# TODO: Add exception handling
# TODO: Add constants to top
# TODO: Change into Class

# function to convert given coord from COIN to +/- decimal degrees
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
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)

    # haversine formula 
    dlong = long2 - long1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong/2)**2
    c = 2 * math.asin(math.sqrt(a)) 

    m = earthRadius * c
    return m 

# function that takes mission file name, opens COIN mission report
# and returns list containing target data with attributes
def coinTargetFormatter( name):
    extension = ".xlsx"
    
    filename = name + extension
    
    # open workbook
    book = xlrd.open_workbook(filename, on_demand=True)
    # open sheet
    # ASSUMPTION: There is only one sheet (position 0)
    sh = book.sheet_by_index(0)
    
    # grab mission name for use in target name formatting
    # ASSUMPTION: Always in position 0x0
    missionName = sh.cell_value(rowx=0, colx=0)
    
    # split mission name based on " "
    missionName = missionName.split(" ")
    
    # ASSUMPTION: Report name format is always the same (position 2)
    missionName = missionName[2]
    # split name into parts
    missionName = missionName.split("-")
    # end result is vehicle number and date
    missionName = missionName[0] + "-" + missionName[1]
    
    # list to hold targets
    targets = []
    
    # Find rows containing targets
    # ASSUMPTION: Target row always starts with "CRN: " in column 0
    # ASSUMPTION: Target category is always in column 4
    # ASSUMPTION: Target coordinates are always in column 6
    for row in range(sh.nrows):
        # list to hold target information
        target = []
        # check if valid row and target row
        if sh.cell_value(rowx=row, colx=0) and sh.cell_value(rowx=row, colx=0).startswith("CRN: "):
            # strip off "CRN: " prefix add mission name
            targetName = sh.cell_value(rowx=row, colx=0)
            targetName = targetName.split(" ")
            # add mission name as prefix
            targetName = targetName[1]
            # add mission name to target attribute list
            target.append(missionName)
            # add name to target attribute list
            target.append(targetName)
            # grab target type from current row
            targetType = sh.cell_value(rowx=row, colx=4)
            # add type to target attribute list
            target.append(targetType)
            # grab target coord from current row
            targetCoord = sh.cell_value(rowx=row, colx=6)
            # split coord into LAT and LONG
            targetCoord = targetCoord.split(",")
            # lat first then long
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
# function to print target list with attributes to console 
# for debugging
def printTargets( targetList):
    # print targets
    for target in targetList:
        for attribute in target:
            print attribute, 
        print "\n"
        break
            
# function for comparing two COIN PMD missions and
# writing output to csv file
# TODO: extend to any number of missions (list of target lists as input)
def compareOutput( missionOne, missionTwo, maxDist, outputName):
    # extension of output file, CSV
    outputName = outputName + ".csv"
    # create / open output file in write mode
    fout = open(outputName, 'w')
    missionOneName = missionOne[0][0]
    missionTwoName = missionTwo[0][0]
    # Mission 1 only targets
    fout.write("Targets present only in " + missionOneName + "\n")
    fout.write("Mission, Target Name, Category, LAT, LONG\n")
    for a in missionOne:
        present = False
        for b in missionTwo:
            if haversine(a[3], a[4], b[3], b[4]) < maxDist:
                present = True
        if present == False:
            fout.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "," + str(a[4]) + "\n")
    fout.write("\n")     
    # Mission 2 only targets 
    fout.write("Targets present only in " + missionTwoName + "\n")
    fout.write("Mission, Target Name, Category, LAT, LONG\n")
    for a in missionTwo:
        present = False
        for b in missionOne:
            if haversine(a[3], a[4], b[3], b[4]) < maxDist:
                present = True
        if present == False:
            fout.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "," + str(a[4]) + "\n")
    fout.write("\n")     
    # Mission 1 and Mission 2 within maxDist
    fout.write("Targets present in both mission " + missionOneName + " and " + missionTwoName + " within distance of " + str(maxDist) + "m\n")
    fout.write("Mission, Target Name, Category, LAT, LONG, Distance\n")
    for a in missionOne:
        for b in missionTwo:
            if haversine(a[3], a[4], b[3], b[4]) < maxDist:
                fout.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "," + str(a[4]) + "," + str(haversine(a[3], a[4], b[3], b[4])) + "\n")
                fout.write(str(b[0]) + "," + str(b[1]) + "," + str(b[2]) + "," + str(b[3]) + "," + str(b[4]) + "\n")
                fout.write(",\n")
