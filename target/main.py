import formatter

# max threshold distance between target and ground truth to state they are the same (m)
max_dist = 40

# name of ground truth PMD Report 
ground_truth = "VxWorks FAT Region"

# name of operator mission PMD Report for analysis
mission_one = "TargetCalls"

name_three = "Mission 1 06274 002 Ascent"

# name of output file
output_name = "CLA"

# build ground truth list from input XML file
#list_one = formatter.contact_parser(ground_truth)

# build contact list from mission XML file
#list_two = formatter.contact_parser(mission_one)

#formatter.print_contacts(list_one) 

#formatter.print_contacts(list_two)

# build output comparison from target lists
#formatter.contact_localization(list_one, list_two, max_dist, output_name)

#formatter.contact_parser(name_two)

#formatter.ctd_parser(name_three)

#formatter.vip_output(list_one, "VxWorks")

temp = formatter.end_point(32.56203, -117.11458, 300, 15000)
print temp
