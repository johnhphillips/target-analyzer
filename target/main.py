import formatter

# max threshold distance between target and ground truth to state they are the same (m)
maxDist = 40

# name of ground truth PMD Report 
groundTruth = "Mission 1"

# name of operator mission PMD Report for analysis
missionOne = "M2"

nameThree = "Mission 1 06274 002 Ascent"

# name of output file
outputName = "CLA"

# build ground truth list from input XML file
listOne = formatter.contactParser(groundTruth)

# build contact list from mission XML file
listTwo = formatter.contactParser(missionOne)

#formatter.printContacts(listOne) 

formatter.printContacts(listTwo)

# build output comparison from target lists
formatter.contactLocalization( listOne, listTwo, maxDist, outputName)

#formatter.contactParser(nameTwo)

#formatter.ctdParser(nameThree)
