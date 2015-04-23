from math import radians, sin, cos, asin, sqrt, pow, atan2, degrees
from myattributes import *
import xml.etree.cElementTree as ET

# TODO: Add exception handling
# TODO: Change into contact class
# TODO: Add constants to top
# TODO: Move CTD parsing to new class (svp)

# function that returns great circle distance between two
# points on the earth (input must be in decimal degrees)
def haversine(lat_1, long_1, lat_2, long_2):
    # in meters
    EARTH_RADIUS = 6378100
    
    # convert decimal degrees to radians 
    lat_1 = radians(lat_1)
    long_1 = radians(long_1)
    lat_2 = radians(lat_2)
    long_2 = radians(long_2)

    # haversine formula 
    d_long = long_2 - long_1 
    d_lat = lat_2 - lat_1 
    a = sin(d_lat/2)**2 + cos(lat_1) * cos(lat_2) * sin(d_long/2)**2
    c = 2 * asin(sqrt(a)) 

    m = EARTH_RADIUS * c
    return m 

# function that returns destination point on earth
# given start point, bearing, distance (decimal degrees,
# decimal degrees, meters)
def end_point(lat_1, long_1, bearing, distance):
    # in meters
    EARTH_RADIUS = 6378100.
    
    # convert decimal degrees to radians 
    lat_1 = radians(lat_1)
    long_1 = radians(long_1)
    bearing = radians(bearing)
    print bearing
    
    # find destination point
    lat_2 = asin(sin(lat_1) * cos(distance / EARTH_RADIUS) + cos(lat_1) * sin(distance / EARTH_RADIUS) * cos(bearing))
    long_2 = long_1 + atan2(sin(bearing) * sin(distance / EARTH_RADIUS) * cos(lat_1), cos(distance / EARTH_RADIUS) - sin(lat_1) * sin(lat_2))
    
    
    
    lat_2 = degrees(lat_2)
    long_2 = degrees(long_2)
    
    return (lat_2, long_2)


# function to print contact list with attributes to console 
# for debugging
def print_contacts(contacts):
    # print contacts
    for contact in contacts:
        for attribute in contact:
            print attribute
        print "\n"
        #break
   

# function for comparing two XML contact files (ground truth vs.
# mission) and writing output to csv file

# TODO: extend to any number of missions (list of contact lists as input)
def contact_localization(mission_one, mission_two, max_dist, file_name):
    # extension of output file, csv
    output_name = file_name + ".csv"
    # create / open output file in write mode
    fout = open(output_name, 'w')
    
    # Print contact matches to ground truth position within maxDist
    fout.write('Contact matches to ground truth position within distance of ' + str(max_dist) + ' m\n')
    fout.write('ID, CRN, LAT, LONG, MATCH, Hd, Vd, Hd^2,, Vd^2\n')
    
    matches = 0
    horz_squared_total = 0
    vert_squared_total = 0
    
    for a in mission_one:
        for b in mission_two:
            horz_dist = haversine(a[2], a[3], b[2], b[3])
            if horz_dist < max_dist:
                # increment matches
                matches = matches + 1
                # check that depth is present for ground truth
                
                if len(a) == 6:
                    # find vertical distance with ground truth at 0
                    vert_dist = a[5] - b[5]
                    vert_squared = pow(vert_dist, 2)
                    vert_squared_total = vert_squared_total + vert_squared
                    
                else:
                    vert_dist = 1
                    vert_squared = 1
                    vert_squared_total = 1
                                
                horz_squared = pow(horz_dist, 2)
                horz_squared_total = horz_squared_total + horz_squared         
                
                fout.write(str(b[0]) + ',' + str(b[1]) + ',' + str(b[2]) + ',' + 
                           str(b[3]) + ',' + str(a[1]) + ',' + str(horz_dist) + ',' + 
                           str(vert_dist) + ',' + str(horz_squared) + ',,' + str(vert_squared) + '\n')
                
    horz_cla = sqrt(horz_squared_total / matches)
    vert_cla = sqrt(vert_squared_total / matches)
           
    fout.write(',,,,,,HCLA,' + str(horz_cla) + ',VCLA,' + str(vert_cla) + '\n')
    fout.write('\n')
    
    # Print false alarms 
    fout.write('False alarms\n')
    fout.write('ID, CRN, LAT, LONG\n')
    for a in mission_two:
        present = False
        for b in mission_one:
            horz_dist = haversine(a[2], a[3], b[2], b[3])
            if horz_dist < max_dist:
                present = True
        if present == False:
            fout.write(str(a[0]) + ',' + str(a[1]) + ',' + str(a[2]) + ',' + str(a[3]) + '\n')
    fout.write('\n')     
    
    fout.close()
    
# function for parsing contact XML file
def contact_parser(file_name):
    # extension of input file, XML
    input_name = file_name + ".xml"
    
    FEET_TO_METERS = 0.3048
    METERS_TO_FEET = 3.28084
    
    # list to hold targets
    contacts = []
    
    message = ET.ElementTree(file=input_name)
    
    for tContact in message.iter(tag = XML_contact):
        # list to hold contact attributes
        contact = []
        
        for attribute in tContact.iter():
            
            if attribute.tag == XML_contact:
                # add ID to contact attribute list
                contact.append(str(attribute.attrib[XML_contact_id]))
                
            if attribute.tag == XML_contact_crn:
                # add CRN to contact attribute list
                contact.append(attribute.text)
                
            if attribute.tag == XML_contact_lat:
                #TODO: Add attribute units check
                contact.append(float(attribute.text))

            if attribute.tag == XML_contact_lon:
                #TODO: Add attribute units check
                contact.append(float(attribute.text))
#                print attribute.attrib['units']
                
            if attribute.tag == XML_contact_kind:
                contact.append(attribute.text)

            if attribute.tag == XML_contact_depth:
                if attribute.attrib[XML_contact_depth_units] == 'ft':
                    depth = float(attribute.text) * FEET_TO_METERS
                    contact.append(depth)
                    
                # otherwise assume case depth is in meters
                else:
                    contact.append(float(attribute.text))
        
        contacts.append(contact)        
    
    return contacts
    
# function for parsing Neil Brown CTD csv file (ascent or decent removed by hand)
def ctd_parser(file_name):
    from time import localtime
    # extension of output file, XML
    output_name = file_name + ".xml"
    # extension of input file, csv
    input_name = file_name + ".csv"
    
    METERS_TO_FEET = 3.28084
      
    # build timestamp    
    current_time = localtime() 
    date = str(current_time[0]) + "-" + str('%02.d' % current_time[1]) + "-" + str('%02.d' % current_time[2])
    times =  "T" + str('%02.d' % current_time[3]) + ":" + str('%02.d' % current_time[4]) + ":" + str('%02.d' % current_time[5]) +".000-08:00" 
    time_stamp = date + times
    
    # open file
    file = open(input_name, 'r')
    # empty list of rows
    rows = []
        
    for line in file:
        # empty row of attributes
        row = []
        
        current_row = line.split(',')
        
        #TODO: search for appropriate attribute column
        lat = current_row[0]
        row.append(lat)
        lon = current_row[1]
        row.append(lon)
        depth = current_row[3]
        row.append(depth)
        salinity = current_row[6]
        row.append(salinity)
        temperature = current_row[5]
        row.append(temperature)
        sound_speed = current_row[7]
        row.append(sound_speed)
        
        rows.append(row)
        
    file.close()
    
    # grab start and end lat/lon    
    start_lat = float(rows[1][0])
    start_lon = float(rows[1][1])
    end_lat = float(rows[len(rows) - 1][0])
    end_lon = float(rows[len(rows) - 1][1])
    
    radius = haversine(start_lat, start_lon, end_lat, end_lon)
    
    # create / open output file in write mode
    fout = open(output_name, 'w')
    
    # add header information to XML file
    fout.write(XML_version)
    fout.write(XML_open_miw)
    fout.write(XML_open_header)
    fout.write(XML_source)
    fout.write(XML_open_timestamp + time_stamp + XML_close_timestamp)
    fout.write(XML_open_classification)
    fout.write(XML_classification_level)
    fout.write(XML_close_classification)
    fout.write(XML_close_header)
    
    fout.write(XML_open_environment)
    fout.write(XML_open_properties)
    fout.write(XML_open_position)
    fout.write(XML_open_lat + str(start_lat) + XML_close_lat)
    fout.write(XML_open_lon + str(start_lon) + XML_close_lon)
    fout.write(XML_close_position)
    fout.write(XML_open_observ + time_stamp + XML_close_observ)
    
    fout.write(XML_open_circle_region)
    fout.write(XML_open_region_name + file_name + XML_close_region_name)
    fout.write(XML_open_circle_geo)
    fout.write(XML_open_position)
    fout.write(XML_open_lat + str(start_lat) + XML_close_lat)
    fout.write(XML_open_lon + str(start_lon) + XML_close_lon)
    fout.write(XML_close_position)
    fout.write(XML_open_radius + str(radius * METERS_TO_FEET) + XML_close_radius)
    fout.write(XML_close_circle_geo)
    fout.write(XML_close_circle_region)  
    
    # add environmental data to XML file
    count = 0 
    for row in rows: 
        # skip header (first) row
        if count == 0:
            count = count + 1
            continue
        fout.write(XML_open_SVP)
        fout.write(XML_open_depth + str(float(row[2]) * METERS_TO_FEET) + XML_close_depth)
        fout.write(XML_open_salinity + row[3] + XML_close_salinity)
        fout.write(XML_open_water_temp + str(float(row[4]) * 1.8 + 32) + XML_close_water_temp)
        fout.write(XML_open_sound_speed + str(float(row[5]) * METERS_TO_FEET) + XML_close_sound_speed)
        fout.write(XML_close_SVP)
        
    fout.write(XML_close_properties)
    fout.write(XML_close_environment)
    fout.write(XML_close_miw)
    
    fout.close()
    
def vip_output(contacts, file_name):
    # extension of VIP local waypoint file
    VIP_extension = '.ini'
    output_name = file_name + VIP_extension
    # create / open output file in write mode
    fout = open(output_name, 'w')
    
    for a in contacts:
        # Contact ID as comment
        fout.write(VIP_comment + a[0] + '\n')
        fout.write(VIP_location + '\n')
        fout.write(VIP_label + a[1] + '\n')
        
        # check for LAT sign and format
        if a[2] > 0:
            lat = '%.5f' % a[2] + 'N'
        elif a[2] < 0:
            temp = a[2] * -1
            lat = '%.5f' % -1 * temp + 'S'
            
        # check of LONG sign and format
        if a[3] > 0:
            lon = '%.5f' % a[3] + 'E'
        elif a[3] < 0:
            temp = a[3] * -1
            lon = '%.5f' % temp + 'W'
            
        fout.write(VIP_position + lat + ' ' + lon + '\n')
        fout.write(VIP_offset_direction + '\n')
        fout.write(VIP_offset_distance + '\n')
        fout.write(VIP_offset_Y + '\n')
        fout.write('\n') 
        
    fout.close()
        