# target-analyzer sandbox 
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

import xlrd
import os
import win32com.client
import myattributes as MA

from target.analyzer import _haversine

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
    
    radius = _haversine(start_lat, start_lon, end_lat, end_lon)
    
    # create / open output file in write mode
    fout = open(output_name, 'w')
    
    # add header information to XML file
    fout.write(MA.XML_version)
    fout.write(MA.XML_open_miw)
    fout.write(MA.XML_open_header)
    fout.write(MA.XML_source)
    fout.write(MA.XML_open_timestamp + time_stamp + MA.XML_close_timestamp)
    fout.write(MA.XML_open_classification)
    fout.write(MA.XML_classification_level)
    fout.write(MA.XML_close_classification)
    fout.write(MA.XML_close_header)
    
    fout.write(MA.XML_open_environment)
    fout.write(MA.XML_open_properties)
    fout.write(MA.XML_open_position)
    fout.write(MA.XML_open_lat + str(start_lat) + MA.XML_close_lat)
    fout.write(MA.XML_open_lon + str(start_lon) + MA.XML_close_lon)
    fout.write(MA.XML_close_position)
    fout.write(MA.XML_open_observ + time_stamp + MA.XML_close_observ)
    
    fout.write(MA.XML_open_circle_region)
    fout.write(MA.XML_open_region_name + file_name + MA.XML_close_region_name)
    fout.write(MA.XML_open_circle_geo)
    fout.write(MA.XML_open_position)
    fout.write(MA.XML_open_lat + str(start_lat) + MA.XML_close_lat)
    fout.write(MA.XML_open_lon + str(start_lon) + MA.XML_close_lon)
    fout.write(MA.XML_close_position)
    fout.write(MA.XML_open_radius + str(radius * METERS_TO_FEET) + MA.XML_close_radius)
    fout.write(MA.XML_close_circle_geo)
    fout.write(MA.XML_close_circle_region)  
    
    # add environmental data to XML file
    count = 0 
    for row in rows: 
        # skip header (first) row
        if count == 0:
            count = count + 1
            continue
        fout.write(MA.XML_open_SVP)
        fout.write(MA.XML_open_depth + str(float(row[2]) * METERS_TO_FEET) + MA.XML_close_depth)
        fout.write(MA.XML_open_salinity + row[3] + MA.XML_close_salinity)
        fout.write(MA.XML_open_water_temp + str(float(row[4]) * 1.8 + 32) + MA.XML_close_water_temp)
        fout.write(MA.XML_open_sound_speed + str(float(row[5]) * METERS_TO_FEET) + MA.XML_close_sound_speed)
        fout.write(MA.XML_close_SVP)
        
    fout.write(MA.XML_close_properties)
    fout.write(MA.XML_close_environment)
    fout.write(MA.XML_close_miw)
    
    fout.close()
    
def vip_output(contacts, file_name):
    # extension of VIP local waypoint file
    VIP_EXTENSION = '.ini'
    output_name = file_name + VIP_EXTENSION
    # create / open output file in write mode
    fout = open(output_name, 'w')
    
    for a in contacts:
        # Contact ID as comment
        fout.write(MA.VIP_comment + a[0] + '\n')
        fout.write(MA.VIP_location + '\n')
        fout.write(MA.VIP_label + a[1] + '\n')
        
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
            
        fout.write(MA.VIP_position + lat + ' ' + lon + '\n')
        fout.write(MA.VIP_offset_direction + '\n')
        fout.write(MA.VIP_offset_distance + '\n')
        fout.write(MA.VIP_offset_Y + '\n')
        fout.write('\n') 
        
    fout.close()

def rangeTargetFormatter( name):
    # 'C:/Users/jphilips/Documents/GitHub/target-compare/target-compare/test3.xlsx'
    # 'C:/Users/jphilips/Documents/GitHub/target-compare/target-compare/test3.xls'
  
    # TODO: Move all numbers to the top
    # TODO: Make target class
    oldExtension = '.xlsx'
    newExtension = '.xls'
    oldFilename = name + oldExtension
    newFilename = name + newExtension
    
    # CONVERT FROM .xlsx to .xls file
    xl = win32com.client.DispatchEx("Excel.Application")
    xl.DisplayAlerts = False
    wb = xl.Workbooks.Open(os.path.join(os.getcwd(), oldFilename))
    
    wb.SaveAs(os.path.join(os.getcwd(), newFilename), FileFormat = 56)
    wb.Close()
    xl.Quit()
    
    # open workbook
    book = xlrd.open_workbook(newFilename, formatting_info=True)
    # open sheet
    # ASSUMPTION: The only sheet of concern is the first one (newest)
    sh = book.sheet_by_index(0)
        
    # list to hold targets
    targets = []
    
    # move down rows in worksheet looking for targets staring at row 4
    for row in range(3, sh.nrows):
        # list to hold target information
        target = []
        # grab extended formatting for first cell in current row
        # ASSUMPTION: Formating information extends across row includes first cell
        xf = book.xf_list[sh.cell_xf_index(row,0)]
        # grab font color tuple for first cell (xxx, xxx, xxx)
        cellColor = book.colour_map[book.font_list[xf.font_index].colour_index]
        # First check that row is valid
        # ASSUMPTION: Black color font (0,0,0) valid
        # ASSUMPTION: No color (automatic) font "None" valid
        # ASSUMPTION: Red color font (255, 0, 0) invalid (Not verified)
        # ASSUMPTION: Blue color font (0, 0, 255) invalid (Status Unknown)
        if (cellColor == (0, 0, 0) or cellColor == None) and sh.cell_value(rowx=row, colx=0):
            # Second check that row if valid
            # ASSUMPTION: If there is a "Date Recovered" entry in column 11 (L)
            # Grab field name and shift to upper case
            # ASSUMPTION: Field always in column 1 (B)
            targetField = sh.cell_value(rowx=row, colx=1).upper()
            target.append(targetField)
            # Grab target name and shift to upper case
            # ASSUMPTION: Name always in column 2 (C)
            targetName = sh.cell_value(rowx=row, colx=2).upper()
            # replace space with underscore
            targetName = targetName.replace(" ", "_")
            # remove ' from name
            targetName = targetName.replace("'", "")
            target.append(targetName)
            # Grab LAT
            # ASSUMPTION: LAT always in column 8 (I)
            lat = sh.cell_value(rowx=row, colx=8)
            # strip leading spaces
            lat = lat.replace(" ", "")
            lat = lat.encode("ascii", "ignore")
            # split into degree [0] / minute [1]
            try:
                nLat = lat.split("'")
                degree = int(nLat[0])
                minute = float(nLat[1])
            except ValueError:
                print "True Latitude for target " + targetName + " in row " + str(row) + " is formatted incorrectly."
                print "Expected Format: XX'XX.XXX"
                print "Current Format: " + lat
                print "Target not added.\n"
                continue
            # ASSUMPTION: LAT always N (+) (San Diego)
            sign = 1
            targetLat = (sign * (degree + (minute / 60)))
            target.append(targetLat)
            # Grab LONG
            # ASSUMPTION: LONG always in column 9 (J)
            long = sh.cell_value(rowx=row, colx=9)
            # strip leading spaces
            long = long.replace(" ", "")
            long = long.encode("ascii", "ignore")
            # split into degree [0] / minute [1] with exception check
            try:
                nLong = long.split("'")
                degree = int(nLong[0])
                minute = float(nLong[1])
            except ValueError:
                print "True Longitude for target " + targetName + " in row " + str(row) + " is formatted incorrectly."
                print "Expected Format: XXX'XX.XXX"
                print "Current Format: " + long
                print "Target not added.\n"
                continue
            # ASSUMPTION: LONG always W (-) (San Diego)
            sign = -1
            targetLong = (sign * (degree + (minute / 60)))
            target.append(targetLong)
            # add targets to list of targets
            targets.append(target)
            
    # DELETE .xls file
    os.unlink(os.path.join(os.getcwd(), newFilename))
    return targets

def vipOutput( targets, outputName):
    # extension of VIP local waypoint file
    vipEx = ".ini"
    outputName = outputName + vipEx
    # create / open output file in write mode
    for a in targets:
        # Field Location Label
        print '#' + a[0]
        print '[Location]'
        print 'Label=' + a[1]
        # check for LAT sign and format
        if a[2] > 0:
            lat = '%.5f' % a[2] + 'N'
        elif a[2] < 0:
            temp = a[2] * -1
            lat = '%.5f' % -1 * temp + 'S'
        # check of LONG sign and format
        if a[3] > 0:
            long = '%.5f' % a[3] + 'E'
        elif a[3] < 0:
            temp = a[3] * -1
            long = '%.5f' % temp + 'W'
        print 'Position=' + lat + ' ' + long
        print 'Offset direction=0.0'
        print 'Offset distance (Meters)='
        print 'Offset Y axis (Meters)=\n'
#         break

def coin_output( file_name):
    from time import localtime
    # extension of output file, XML
    output_name = file_name + ".xml"
    # extension of input file, csv
    input_name = file_name + ".csv"
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
        name = current_row[0]
        if name == '':
            continue
        row.append(name)
        lat = current_row[1]
        row.append(lat)
        lon = current_row[2]
        lon = lon.replace('\n', '')
        row.append(lon)
       
        
        rows.append(row)
        
    file.close()
    
    # create / open output file in write mode
    fout = open(output_name, 'w')
    
    # add header information to XML file
    fout.write(MA.XML_version + '\n')
    fout.write(MA.XML_open_miw + '\n')
    fout.write(MA.XML_open_header + '\n')
    fout.write(MA.XML_source + '\n')
    fout.write(MA.XML_open_timestamp + time_stamp + MA.XML_close_timestamp + '\n')
    fout.write(MA.XML_open_classification + '\n')
    fout.write(MA.XML_classification_level + '\n')
    fout.write(MA.XML_close_classification + '\n')
    fout.write(MA.XML_close_header + '\n')
    fout.write(MA.XML_open_contact_list + '\n')
    
    # add target data to XML file
    count = 0 
    for row in rows: 

        fout.write(MA.XML_open_tac_contact + str(row[0]) + '\">' + '\n')
        fout.write(MA.XML_open_CRN + 'SSC-' + str('%03d' % (count + 1)) + MA.XML_close_CRN + '\n')
        fout.write(MA.XML_open_position + '\n')
        fout.write(MA.XML_open_lat + str(row[1]) + MA.XML_close_lat + '\n')
        fout.write(MA.XML_open_lon + str(row[2]) + MA.XML_close_lon + '\n')
        fout.write(MA.XML_close_position + '\n')
        fout.write(MA.XML_open_contact_kind + 'MILCO' + MA.XML_close_contact_kind + '\n')
        fout.write(MA.XML_close_tac_contact + '\n')
        count = count + 1
        
    fout.write(MA.XML_close_contact_list + '\n')
    fout.write(MA.XML_close_miw)
        
    fout.close()
    
    