import xlrd
import os
import win32com.client

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
    