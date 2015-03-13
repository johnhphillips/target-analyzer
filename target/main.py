import formatter

# max threshold distance between target and ground truth to state they are the same (m)
maxDist = 40

# name of ground truth PMD Report 
nameOne = "PRB1 Ground Truth"

# name of operator mission PMD Report for analysis
nameTwo = "Soto MSN09"

nameThree = "Mission 1 06274 002 Ascent"

# name of output file
outputName = "Horizontal CLA"

# build contact list from input PMD Reports
listOne = formatter.coinContactFormatter( nameOne) 

listTwo = formatter.coinContactFormatter( nameTwo)

# build output comparison from target lists
formatter.contactLocalization( listOne, listTwo, maxDist, outputName)

#formatter.contactParser(nameTwo)

formatter.ctdParser(nameThree)
