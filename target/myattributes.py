
# variables associated with parsing of contact information in MEDAL XML file
XML_contact = '{http://www.saic.com/navy/miwml.1.0}TacticalContact'
XML_contact_id = 'contact_id'
XML_contact_crn = '{http://www.saic.com/navy/miwml.1.0}CRN'
XML_contact_lat = '{http://www.saic.com/navy/miwml.1.0}Latitude'
XML_contact_lon = '{http://www.saic.com/navy/miwml.1.0}Longitude'
XML_contact_kind = '{http://www.saic.com/navy/miwml.1.0}ContactKind'
XML_contact_depth = '{http://www.saic.com/navy/miwml.1.0}CaseDepth'
XML_contact_depth_units = 'units'
        
# variables associated with building of MEDAL SVP file
XML_version = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'
XML_open_miw = '<Miw xmlns=\"http://www.saic.com/navy/miwml.1.0\">'
XML_open_header = '<MessageHeader>'
XML_source = '<MessageSource>SSCPACIFIC</MessageSource>'
XML_open_timestamp = '<Timestamp>'
XML_close_timestamp = '</Timestamp>'
XML_open_classification = '<Classification>'
XML_classification_level = '<ClassificationLevel>UNCLASSIFIED</ClassificationLevel>'
XML_close_classification = '</Classification>'
XML_close_header = '</MessageHeader>'
XML_close_miw = '</Miw>'

XML_open_environment = '<EnvironmentList>'
XML_open_properties = '<PhysicalProperties environment_id=\"env_000\">'
XML_open_position = '<Position>'
XML_open_lat = '<Latitude units=\"degrees\">'
XML_close_lat = '</Latitude>'
XML_open_lon = '<Longitude units=\"degrees\">'
XML_close_lon = '</Longitude>'
XML_close_position = '</Position>'
XML_open_observ = '<Observation>'
XML_close_observ = '</Observation>'

XML_open_SVP = '<SoundVelocityProfile>'
XML_open_depth = '<Depth units=\"ft\">'
XML_close_depth = '</Depth>'
XML_open_salinity = '<Salinity units=\"ppt\">'
XML_close_salinity = '</Salinity>'
XML_open_water_temp = '<WaterTemperature units=\"Fahrenheit\">'
XML_close_water_temp = '</WaterTemperature>'
XML_open_sound_speed = '<SoundSpeed units=\"ft/s\">'
XML_close_sound_speed = '</SoundSpeed>'
XML_close_SVP = '</SoundVelocityProfile>'

XML_close_properties = '</PhysicalProperties>'
XML_close_environment = '</EnvironmentList>'

# variables associated with building of MEDAL Circle Region
XML_open_circle_region = '<CircleRegion>'
XML_open_region_name = '<RegionName>'
XML_close_region_name = '</RegionName>'
XML_open_circle_geo = '<CircleGeometry>'
XML_open_radius = '<Radius units=\"ft\">'
XML_close_radius = '</Radius>'
XML_close_circle_geo = '</CircleGeometry>'
XML_close_circle_region = '</CircleRegion>'

# variables associated with building VIP waypoint output
VIP_comment = '#'
VIP_location = '[Location]'
VIP_label = 'Label='
VIP_position = 'Position='
VIP_offset_direction = 'Offset direction=0.0'
VIP_offset_distance = 'Offset distance (Meters)='
VIP_offset_Y = 'Offset Y axis (Meters)='





