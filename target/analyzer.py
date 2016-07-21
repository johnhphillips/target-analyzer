# target-analyzer, functions to support analysis of contact information 
# Copyright (C) 2015 John Phillips, SPAWAR Systems Center Pacific
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from math import radians, sin, cos, asin, sqrt, pow, atan2, degrees
import myattributes as MA
import xml.etree.ElementTree as ET

# TODO: Add exception handling
# TODO: Add get functions for constants

EARTH_RADIUS = 6378100.
EPSILON = 0.00002

FEET_TO_METERS = 0.3048
METERS_TO_FEET = 3.28084


# helper function that returns great circle distance between two
# points on the earth (input must be in decimal degrees)
def _haversine(lat_1, long_1, lat_2, long_2):
    
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

# helper function that returns angular distance given distance; 
# distance is assumed to be in meters
def _angular_distance(distance):
    return distance / EARTH_RADIUS

def _average(num_set): 
    if len(num_set) > 1: 
        return (sum(num_set) * 1.0 / len(num_set))
    else: 
        return num_set

def _variance(num_set):
    total = 0
    avg = _average(num_set)
    if len(num_set) == 1:
        return total
    for item in num_set:
        total = total + (item - avg)**2
    
    return total / (len(num_set) - 1)

def _stdev(num_set): return sqrt(_variance(num_set))

def _stderror(num_set): 
    if len(num_set) > 1:
        return _stdev(num_set) / sqrt(len(num_set))
    else:
        return 0

# helper function that check if given coordinate pair are different
# using epsilon value, then rounds coord_2 to 5 sig figs; assumed to  
# be in decimal degrees and decimal degrees input 
def _coord_check(coord_1, coord_2):  
    if coord_2 - coord_1 < EPSILON:
        coord_2 = coord_1

    coord_2 = round(coord_2, 5)
    return coord_2

# helper function that return bearing from start lat/long
# to end lat/long (input must be in decimal degrees)
def _bearing(lat_1, long_1, lat_2, long_2):
    
    # convert decimal degrees to radians 
    lat_1 = radians(lat_1)
    long_1 = radians(long_1)
    lat_2 = radians(lat_2)
    long_2 = radians(long_2)
    
    bearing = atan2(sin(long_2-long_1)*cos(lat_2), cos(lat_1)*sin(lat_2)-sin(lat_1)*cos(lat_2)*cos(long_2-long_1))
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360
    
    return bearing

# function that returns destination point on earth
# given start lat, long, bearing, and distance; 
# assumed to be decimal degrees, decimal degrees, degrees
# and meters input
def end_point(lat_1, long_1, bearing, distance): 
    is_negative = False 
    # convert decimal degrees to radians 
    lat_1 = radians(lat_1)
    long_1 = radians(long_1)
    if long_1 < 0:
        is_negative = True
        long_1 = long_1 * -1
    
    bearing = radians(bearing)
    # find destination point
    lat_2 = asin(sin(lat_1) * cos(distance / EARTH_RADIUS) + cos(lat_1) * sin(distance / EARTH_RADIUS) * cos(bearing))
    long_2 = long_1 + atan2(sin(bearing) * sin(distance / EARTH_RADIUS) * cos(lat_1), cos(distance / EARTH_RADIUS) - sin(lat_1) * sin(lat_2))
    #a = _angular_distance(distance)
    # find destination point
    #lat_2 = asin(sin(lat_1) * cos(a) + cos(lat_1) * sin(a) * cos(bearing))
    #long_2 = long_1 + atan2(sin(bearing) * sin(a) * cos(lat_1), cos(a) - sin(lat_1) * sin(lat_2))
    
    lat_2 = degrees(lat_2)
    
    lat_2 = _coord_check(lat_1, lat_2)    
    
    long_2 = degrees(long_2)
    
    long_2 = _coord_check(long_1, long_2)
    
    if is_negative == True:
        long_2 = long_2 * -1
        
    return (lat_2, long_2)


# function to print contact list with attributes to console 
# for debugging
def _print_contacts(contacts):
    # print contacts
    for contact in contacts:
        for attribute in contact:
            print attribute
        print "\n"
        #break
   

# function for comparing two XML contact files (ground truth vs.
# mission) and writing output to csv file

# TODO: extend to any number of missions (list of contact lists as input)
# TODO: catch error case of no matches, better than hard code

def contact_localization(ground_truth, contacts, max_dist, output_name):
    # create / open output file in write mode
    fout = open(output_name, 'w')
    
    # Print contact matches to ground truth position within maxDist
    fout.write('Contact matches to ground truth position within distance of ' + str(max_dist) + ' m\n')
    fout.write('ID, CRN, LAT, LONG, MATCH, Hd, Vd, BEARING, Hd^2,, Vd^2\n')
    
    matches = 0
    horz_squared_total = 0
    horz_dists = []
    vert_squared_total = 0
    vert_dists = []
    
    # calculate CLA
    for a in ground_truth:
        for b in contacts:
            horz_dist = _haversine(a[2], a[3], b[2], b[3])
            if horz_dist < max_dist:
                # increment matches
                matches = matches + 1
                bearing = _bearing(a[2], a[3], b[2], b[3])
                
                horz_dists.append(horz_dist)
                # check that ground truth shape is moored 
                # and depth is present in position 6.
                if a[4] == 'Mine-Moored':# and len(a) == 5:
                    # find vertical distance with ground truth at 0
                    vert_dist = a[5] - b[5]
                    vert_squared = pow(vert_dist, 2)
                    vert_squared_total = vert_squared_total + vert_squared
                    
                    vert_dists.append(vert_dist)
                    
                else:
                    vert_dist = 'N/A'
                    vert_squared = 'N/A'
                    
                                
                horz_squared = pow(horz_dist, 2)
                horz_squared_total = horz_squared_total + horz_squared         
                
                fout.write(str(b[0]) + ',' + str(b[1]) + ',' + str(b[2]) + ',' + 
                           str(b[3]) + ',' + str(a[1]) + ',' + str(horz_dist) + ',' + 
                           str(vert_dist) + ',' + str(bearing) + ',' + str(horz_squared) + ',,' + str(vert_squared) + '\n')
    # TODO: Rework method with try/catch handling
    if matches > 0:            
        horz_cla = sqrt(horz_squared_total / matches)
        vert_cla = sqrt(vert_squared_total / matches)
        
    else:
        horz_cla = horz_squared_total
        vert_cla = vert_squared_total
    
    # TODO: case of no matches
    # TODO: case of no vertical matches  
    fout.write(',,,,,,,HCLA,' + str(horz_cla) + ',VCLA,' + str(vert_cla) + '\n')
    print horz_dists
    fout.write(',,,,,,,HStdev,' + str(_stdev(horz_dists)) + ',VStdev,' + str(_stdev(vert_dists)) + '\n')
    fout.write(',,,,,,,HCI,' + str(_stderror(horz_dists) * 1.98) + ',VCI,' + str(_stderror(vert_dists) * 1.98) + '\n')
    fout.write('\n')
    
    # Calculate Search Level 
    fout.write('Search Level\n')
    fout.write('ID, CRN, FOUND\n')
    targets = 0
    called = 0
    for a in ground_truth:
        found = False
        
        for b in contacts:
            horz_dist = _haversine(a[2], a[3], b[2], b[3])
            if horz_dist < max_dist:
                if a[4] == 'Mine-Bottom' and (b[4] == 'MILCO' or b[4] == 'MILCO-Bottom'):
                    found = True
                    called = called + 1
                    break
        if a[4] == 'Mine-Bottom':
            targets = targets + 1
            fout.write(str(a[0]) + ',' + str(a[1]) + ',' + str(found) + '\n')    
    if targets > 0:
        search_level = float(called) / targets

    else:
        search_level = 0
    
    fout.write('Search Level = ' + str(search_level) + '\n')
    fout.write('\n')
    
    # Calculate False Alarm Search Level
    fout.write('False Alarm Search Level\n')
    fout.write('ID, CRN, CALLED MILCO\n')
    distractors = 0
    count = 0
    for a in ground_truth:
        called = False
        
        for b in contacts:
            horz_dist = _haversine(a[2], a[3], b[2], b[3])
            if horz_dist < max_dist:
                if a[4] == 'Non-MILCO' and (b[4] == 'MILCO' or b[4] == 'MILCO-Bottom'):
                    called = True
                    count = count + 1
        if a[4] == 'Non-MILCO':
            distractors = distractors + 1
            fout.write(str(a[0]) + ',' + str(a[1]) + ',' + str(called) + '\n')
        
    if targets > 0:
        search_level = float(count) / targets
    else:
        search_level = 0
    
    fout.write('False Alarm Search Level = ' + str(search_level) + '\n')
    fout.write('\n')        
    
    # Print false alarms 
    calls = 0
    fout.write('False Positive Level\n')
    fout.write('ID, CRN, LAT, LONG\n')
    for a in contacts:
        present = False
        for b in ground_truth:
            # remove matches
            horz_dist = _haversine(a[2], a[3], b[2], b[3])
            if horz_dist < max_dist:
                present = True
            
        if present == False:
            calls = calls + 1
            fout.write(str(a[0]) + ',' + str(a[1]) + ',' + str(a[2]) + ',' + str(a[3]) + '\n')

    if calls > 0:
        false_level = float(calls) / (targets + distractors)
    else:
        false_level = 0

    fout.write('False Positive Level = ' + str(false_level) + '\n')
    fout.write('\n')     
    fout.close()
    
# function for parsing contact XML file
def contact_parser(input_name):  
    # list to hold targets
    contacts = []
    
    message = ET.ElementTree(file = input_name)
    
    for tContact in message.iter(tag = MA.XML_contact):
        # list to hold contact attributes
        contact = []
        
        for attribute in tContact.iter():
            
            if attribute.tag == MA.XML_contact:
                # add ID to contact attribute list
                contact.append(str(attribute.attrib[MA.XML_contact_id]))
                
            if attribute.tag == MA.XML_contact_crn:
                # add CRN to contact attribute list
                contact.append(attribute.text)
                
            if attribute.tag == MA.XML_contact_lat:
                #TODO: Add attribute units check
                contact.append(float(attribute.text))

            if attribute.tag == MA.XML_contact_lon:
                #TODO: Add attribute units check
                contact.append(float(attribute.text))
#                print attribute.attrib['units']
                
            if attribute.tag == MA.XML_contact_kind:
                contact.append(attribute.text)

            if attribute.tag == MA.XML_contact_depth:
                if attribute.attrib[MA.XML_contact_depth_units] == 'ft':
                    depth = float(attribute.text) * FEET_TO_METERS
                    contact.append(depth)
                    
                # otherwise assume case depth is in meters
                else:
                    contact.append(float(attribute.text))
        
        contacts.append(contact)        
    
    return contacts
    
    