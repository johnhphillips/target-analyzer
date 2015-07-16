from target import analyzer
import math

# max threshold distance between target and ground truth to state they are the same (m)
max_dist = 40

# name of ground truth PMD Report 
ground_truth = "VxWorks ATLAS GT.xml"

# name of operator mission PMD Report for analysis
mission_one = "SW 06225 FLS005.xml"

# name of output file
output_name = "CLA.csv"

# build ground truth list from input XML file
list_one = analyzer.contact_parser(ground_truth)

# build contact list from mission XML file
list_two = analyzer.contact_parser(mission_one)

analyzer._print_contacts(list_one) 

analyzer._print_contacts(list_two)

# build output comparison from target lists
analyzer.contact_localization(list_one, list_two, max_dist, output_name)


#temp = analyzer.end_point(32.56203, -117.11458, 300, 15000)
#print temp[0]
#print temp[1]
