from math import radians, sin, cos, asin, sqrt, pow
import xml.etree.cElementTree as ET

# TODO: Add exception handling
# TODO: Add constants to top
# TODO: Change into Class

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

# function to print contact list with attributes to console 
# for debugging
def printContacts( contactList):
    # print contacts
    for contact in contactList:
        for attribute in contact:
            print attribute
        print "\n"
        #break


            
# function for comparing two MEDAL XML contact files (ground truth vs.
# mission) and writing output to csv file

# TODO: extend to any number of missions (list of target lists as input)
def contactLocalization( missionOne, missionTwo, maxDist, outputName):
    # extension of output file, CSV
    outputName = outputName + ".CSV"
    # create / open output file in write mode
    fout = open(outputName, 'w')
    
    # Print contact matches to ground truth position within maxDist
    fout.write("Contact matches to ground truth position within distance of " + str(maxDist) + " m\n")
    fout.write("ID, CRN, LAT, LONG, MATCH, Hd, Vd, Hd^2,, Vd^2\n")
    
    matches = 0
    h2Total = 0
    v2Total = 0
    
    for a in missionOne:
        for b in missionTwo:
            horzDist = haversine(a[2], a[3], b[2], b[3])
            if horzDist < maxDist:
                # increment matches
                matches = matches + 1
                # check that depth is present for ground truth
                
                if len(a) == 6:
                    # find vertical distance with ground truth at 0
                    vertDist = a[5] - b[5]
                    v2 = pow(vertDist, 2)
                    v2Total = v2Total + v2
                    
                else:
                    vertDist = 1
                    v2 = 1
                    v2Total = 1
                                
                h2 = pow(horzDist, 2)
                h2Total = h2Total + h2         
                
                fout.write(str(b[0]) + "," + str(b[1]) + "," + str(b[2]) + "," + 
                           str(b[3]) + "," + str(a[1]) + "," + str(horzDist) + "," + 
                           str(vertDist) + "," + str(h2) + ",," + str(v2) + "\n")
                
    hCLA = sqrt(h2Total / matches)
    vCLA = sqrt(v2Total / matches)
           
    fout.write(",,,,,,HCLA," + str(hCLA) + ",VCLA," + str(vCLA) + "\n")
    fout.write("\n")
    
    # Print false alarms 
    fout.write("False alarms\n")
    fout.write("ID, CRN, LAT, LONG\n")
    for a in missionTwo:
        present = False
        for b in missionOne:
            horzDist = haversine(a[2], a[3], b[2], b[3])
            if horzDist < maxDist:
                present = True
        if present == False:
            fout.write(str(a[0]) + "," + str(a[1]) + "," + str(a[2]) + "," + str(a[3]) + "\n")
    fout.write("\n")     
    
    fout.close()
    
# function for parsing contact XML file
def contactParser( fileName):
    # extension of input file, XML
    fileName = fileName + ".XML"
    
    ft2m = 0.3048
    m2ft = 3.28084
    
    # list to hold targets
    contacts = []
    
    message = ET.ElementTree(file=fileName)
    
    for tContact in message.iter(tag='{http://www.saic.com/navy/miwml.1.0}TacticalContact'):
        # list to hold contact attributes
        contact = []
        
        for attribute in tContact.iter():
            
            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}TacticalContact':
                # add ID to contact attribute list
                contact.append(str(attribute.attrib['contact_id']))
                
            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}CRN':
                # add CRN to contact attribute list
                contact.append(attribute.text)
                
            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}Latitude':
                #TODO: Add attribute units check
                contact.append(float(attribute.text))

            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}Longitude':
                #TODO: Add attribute units check
                contact.append(float(attribute.text))
#                print attribute.attrib['units']
                
            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}ContactKind':
                contact.append(attribute.text)

            if attribute.tag == '{http://www.saic.com/navy/miwml.1.0}CaseDepth':
                if attribute.attrib['units'] == 'ft':
                    depth = float(attribute.text) * ft2m
                    contact.append(depth)
                    
                # otherwise assume case depth is in meters
                else:
                    contact.append(float(attribute.text))
        
        contacts.append(contact)        
    
    return contacts
    
# function for parsing Neil Brown CTD CSV file (ascent or decent removed by hand)
def ctdParser( fileName):
    from time import localtime
    # extension of output file, XML
    outputName = fileName + ".XML"
    # extension of input file, csv
    inputName = fileName + ".CSV"
    
    meter2feet = 3.28084
      
    # build timestamp    
    currentTime = localtime() 
    date = str(currentTime[0]) + "-" + str('%02.d' % currentTime[1]) + "-" + str('%02.d' % currentTime[2])
    times =  "T" + str('%02.d' % currentTime[3]) + ":" + str('%02.d' % currentTime[4]) + ":" + str('%02.d' % currentTime[5]) +".000-08:00" 
    timeStamp = date + times
    
    # open file
    file = open( inputName, 'r')
    # empty list of rows
    rows = []
        
    for line in file:
        # empty row of attributes
        row = []
        
        currentRow = line.split(',')
        
        #TODO: search for appropriate attribute column
        lat = currentRow[0]
        row.append(lat)
        lon = currentRow[1]
        row.append(lon)
        depth = currentRow[3]
        row.append(depth)
        salinity = currentRow[6]
        row.append(salinity)
        temperature = currentRow[5]
        row.append(temperature)
        soundSpeed = currentRow[7]
        row.append(soundSpeed)
        
        rows.append(row)
        
    # grab start and end lat/lon    
    startLat = float(rows[1][0])
    startLon = float(rows[1][1])
    endLat = float(rows[len(rows) - 1][0])
    endLon = float(rows[len(rows) - 1][1])
    
    radius = haversine(startLat, startLon, endLat, endLon)
    
    # create / open output file in write mode
    fout = open(outputName, 'w')
    
    # add header information to XML file
    fout.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    fout.write("<Miw xmlns=\"http://www.saic.com/navy/miwml.1.0\">")
    fout.write("<MessageHeader>")
    fout.write("<MessageSource>COINv2</MessageSource>")
    fout.write("<Timestamp>" + timeStamp + "</Timestamp>")
    fout.write("<Classification>")
    fout.write("<ClassificationLevel>UNCLASSIFIED</ClassificationLevel>")
    fout.write("</Classification>")
    fout.write("</MessageHeader>")
    fout.write("<EnvironmentList>")
    fout.write("<PhysicalProperties environment_id=\"env_000\">")
    fout.write("<Position><Latitude units=\"degrees\">" + str(startLat) + "</Latitude>")
    fout.write("<Longitude units=\"degrees\">" + str(startLon) + "</Longitude>")
    fout.write("</Position>")
    fout.write("<Observation>" + timeStamp + "</Observation>")
    fout.write("<CircleRegion>")
    fout.write("<RegionName>" + fileName + "</RegionName>")
    fout.write("<CircleGeometry>")
    fout.write("<Position>")
    fout.write("<Latitude units=\"degrees\">" + str(startLat) + "</Latitude>")
    fout.write("<Longitude units=\"degrees\">" + str(startLon) + "</Longitude>")
    fout.write("</Position>")
    fout.write("<Radius units=\"ft\">" + str(radius * meter2feet) + "</Radius>")
    fout.write("</CircleGeometry>")
    fout.write("</CircleRegion>")  
    
    # add environmental data to XML file
    count = 0 
    for row in rows: 
        # skip header (first) row
        if count == 0:
            count = count + 1
            continue
        fout.write("<SoundVelocityProfile>")
        fout.write("<Depth units=\"ft\">" + str(float(row[2]) * meter2feet) + "</Depth>")
        fout.write("<Salinity units=\"ppt\">" + row[3] + "</Salinity>")
        fout.write("<WaterTemperature units=\"Fahrenheit\">" + str(float(row[4]) * 1.8 + 32) + "</WaterTemperature>")
        fout.write("<SoundSpeed units=\"ft/s\">" + str(float(row[5]) * meter2feet) + "</SoundSpeed>")
        fout.write("</SoundVelocityProfile>")
        
    fout.write("</PhysicalProperties>")
    fout.write("</EnvironmentList>")
    fout.write("</Miw>")
    
    fout.close()
    
def vipOutput( targets, outputName):
    # extension of VIP local waypoint file
    vipEx = ".ini"
    outputName = outputName + vipEx
    # create / open output file in write mode
    fout = open(outputName, "w")
    for a in targets:
        # Field Location Label
        fout.write("#" + a[0] + "\n")
        fout.write("[Location]" + "\n")
        fout.write("Label=" + a[1] + "\n")
        # check for LAT sign and format
        if a[2] > 0:
            lat = "%.5f" % a[2] + "N"
        elif a[2] < 0:
            temp = a[2] * -1
            lat = "%.5f" % -1 * temp + "S"
        # check of LONG sign and format
        if a[3] > 0:
            lon = "%.5f" % a[3] + "E"
        elif a[3] < 0:
            temp = a[3] * -1
            lon = "%.5f" % temp + "W"
        fout.write("Position=" + lat + " " + lon + "\n")
        fout.write("Offset direction=0.0" + "\n")
        fout.write("Offset distance (Meters)=" + "\n")
        fout.write("Offset Y axis (Meters)=" + "\n" + "\n")
    fout.close()
        