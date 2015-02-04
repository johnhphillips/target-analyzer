import formatter

# max threshold distance between target and ground truth to state they are the same (m)
maxDist = 40

# name of ground truth PMD Report 
nameOne = "PRB1 Ground Truth"

# name of operator mission PMD Report for analysis
nameTwo = "Soto MSN09"

# name of output file
outputName = "Horizontal CLA"

# build contact list from input PMD Reports
listOne = formatter.coinTargetFormatter( nameOne) 
print "-----" 
listTwo = formatter.coinTargetFormatter( nameTwo)

# build output comparison from target lists
formatter.compareOutput( listOne, listTwo, maxDist, outputName)