import xml.etree.ElementTree as ET
tree = ET.parse('export-38335.xml')
root = tree.getroot()

for species in root.findall('species'):
	for common_names in species.findall('common_names'):
		for name in common_names.findall('name'):
			condition = name.get('lang')
			if "Eng" in condition:			
				names = name.text
	for assessment in species.findall('assessment'):
		cat = assessment.find('category').text
	speciesID = species.get('id')
	sciName = species.find('scientific_name').text
	print speciesID
	print sciName
	print names
	print cat
	try:
		pop = species.find('population').text
		print pop
	except AttributeError:
		print 'no population'