# import all the stuff/tools we need 
import urllib2 
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from geopy import geocoders
import re
import time

# open our txt file for the data to go in
file = open('/Users/benarmham/Desktop/iucncodetry/iucn-data2.txt', 'w')

# open the iucn downloaded data
tree = ET.parse('export-38692.xml')
root = tree.getroot()
print 'Getting Data'

# iterate through each species in data
for species in root.findall('species'):	
	
	# find each common name, avoiding french or spanish
	for common_names in species.findall('common_names'):
		for name in common_names.findall('name'):
			condition = name.get('lang')
			if "Eng" in condition:			
				try:
					names = name.text
					print names + ': name - ok'
					file.write(names + '; ')
				except UnicodeEncodeError:
					print 'Name not Unicode' 
					file.write('Common name not unicode' + '; ')

	# find assessment category
	for assessment in species.findall('assessment'):
		cat = assessment.find('category').text
		print cat + ': cat - ok'
		file.write(',' + cat + ',')
	
	# and the species id, scientific names, and class
	speciesID = species.get('id')
	sciName = species.find('scientific_name').text
	sciClass = species.find('class_name').text
	print speciesID + ': ID - ok'
	print sciName + ': scientific name - ok'
	print sciClass + ': class - ok'
	file.write(speciesID + ',' + sciName + ',' + sciClass + ',')
	
	# get population data, allowing for known missing fields
	try:
		pop = species.find('population').text
		print pop + ': population - ok'
	except AttributeError:
		print 'no population data'
		file.write('no pupulation data' + ',')
		continue
	file.write(pop + ',')

	# use species ID to create a url
	url = "http://www.iucnredlist.org/details/" + speciesID + "/0"
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page)
			
	# scrape location from html
	locations = soup.find(attrs={"class":"group"}).get_text(" ", strip=True)
	location = locations + ';'
	print location + ': location - ok' 

	# find type of location (native, possibly extinct, etc)
	loc = re.findall('^(.*?):', location)
	for string in loc:
		description = string
		file.write(description + ',')
	
	# get the country names ready for geocoding
	countries = re.findall(':(.*?)$', location)
	for string in countries:
		eachC = string	
		markers = re.findall('\s(.*?);', eachC)
				
		# remove extra detail that will confuse google unless is needed to differentiate
		for string in markers:
			eachM = string
			if "Congo," in eachM:
				end = re.findall(',\s(.*?)$', eachM)
				for string in end:
					front = string + ' '
				only = eachM.split(',', 1)[0]
				toGeo = front + only
			elif "Korea" in eachM:
				end = re.findall(',\s(.*?)$', eachM)
				for string in end:
					front = string + ' '
				only = eachM.split(',', 1)[0]
				toGeo = front + only
			else:
				only = eachM.split(',', 1)[0]
				toGeo = only.split('(', 1)[0]
					
			# start geocoding, allowing for extra marker errors and name errors
			print "Getting geodata for " + toGeo
			g = geocoders.Google()
			try:
				place, (lat, lng) = g.geocode(toGeo)
				latlon = "%s: %.5f, %.5f" % (place, lat, lng)
				m = re.sub(',', ' ', latlon)
				marker = re.sub('$', ';', m)
				file.write(marker + ' ')
				
				place, (lat, lng) = g.geocode(toGeo)
				latlon = "%s: %.5f, %.5f" % (place, lat, lng)
				marker = re.sub(',', ';', latlon)
				file.write(marker + ' ')
			except ValueError:
				print 'Value Error'
				try:
					file.write("Too many markers for " + toGeo + ' ')
				except UnicodeEncodeError:
					file.write('Name not unicode, cant write ')
					continue
				continue
			
			# wait a moment so the geocoding doesn't get over run
			print "Waiting"
			time.sleep(2)

	# start a new line in the txt ready for the loop to go again
	file.write('\n')

# done getting data! Close file.
file.close()