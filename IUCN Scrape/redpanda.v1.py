import urllib2 
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from geopy import geocoders
import re

# open our txt file for the data to go in
f = open('/Users/benarmham/Desktop/iucncodetry/iucn-data.txt', 'w')

# open the iucn downloaded data
tree = ET.parse('export-38335.xml')
root = tree.getroot()
print 'Getting Data'

#iterate through each species in data, find common name
for species in root.findall('species'):
	for common_names in species.findall('common_names'):
		for name in common_names.findall('name'):
			names = name.text
			print names + ': name - ok'

	# and find assessment category
	for assessment in species.findall('assessment'):
		cat = assessment.find('category').text
		print cat + ': cat - ok'
	
	# and the species id and scientific names
	speciesID = species.get('id')
	sciName = species.find('scientific_name').text
	print speciesID + ': ID - ok'
	print sciName + ': scientific name - ok'
	
	# get population data, allowing for known missing fields
	try:
		pop = species.find('population').text
		print pop + ': population - ok'
	except AttributeError:
		print 'no population data'

	# use species ID to create a url
	url = "http://www.iucnredlist.org/details/" + speciesID + "/0"
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page)
	
	#scrape location from html
	locations = soup.find(attrs={"class":"group"}).get_text(" ", strip=True)
	location = locations + ';'
	print location + ': location - ok' 
	
	# create markers and geocode
	markers = re.findall('\s(.*?);', location)
	for string in markers:
		toGeo = string
		print toGeo
		g = geocoders.Google()
		place, (lat, lng) = g.geocode(toGeo)
		marker = "%s: %.5f, %.5f" % (place, lat, lng)
		print "Getting geodata"
		
	# write data into the file
	f.write(sciName + ',' + speciesID + ',' + names + ',' + cat + ',' + pop + ',' + marker + '\n')

# Done getting data! Close file.
f.close()