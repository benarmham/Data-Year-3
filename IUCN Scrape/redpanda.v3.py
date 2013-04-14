import urllib2 
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from geopy import geocoders
import re
import time

# open our txt file for the data to go in
f = open('/Users/benarmham/Desktop/iucncodetry/iucn-data.txt', 'w')

# open the iucn downloaded data
tree = ET.parse('export-38692.xml')
root = tree.getroot()
print 'Getting Data'

#iterate through each species in data, find common name
for species in root.findall('species'):
	for common_names in species.findall('common_names'):
		for name in common_names.findall('name'):
			condition = name.get('lang')
			if "Eng" in condition:			
				try:
					names = name.text
					print names + ': name - ok'
					f.write(names + '; ')
				except UnicodeEncodeError:
					print 'Name not Unicode' 
					f.write('Common name not unicode' + '; ')

	# and find assessment category
	for assessment in species.findall('assessment'):
		cat = assessment.find('category').text
		print cat + ': cat - ok'
		f.write(',' + cat + ',')
	
	# and the species id and scientific names
	speciesID = species.get('id')
	sciName = species.find('scientific_name').text
	print speciesID + ': ID - ok'
	print sciName + ': scientific name - ok'
	f.write(speciesID + ',' + sciName + ',')
	
	# get population data, allowing for known missing fields
	try:
		pop = species.find('population').text
		print pop + ': population - ok'
	except AttributeError:
		print 'no population data'
		f.write('no pupulation data' + ',')
		continue
	f.write(pop + ',')

	# use species ID to create a url
	url = "http://www.iucnredlist.org/details/" + speciesID + "/0"
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page)
	
	#scrape location from html
	locations = soup.find(attrs={"class":"group"}).get_text(" ", strip=True)
	location = locations + ';'
	print location + ': location - ok' 
	des = re.findall('^(.*?):', location)
	for string in des:
		description = string		
		print description
		f.write(description + ',')
	
	# create markers and geocode
	markers = re.findall(':\s(.*?);', location)
	for string in markers:
		a = string
		b = a.split(',', 1)[0]
		toGeo = b.split('(', 1)[0]
		print "Getting geodata for " + toGeo
		g = geocoders.Google()
		try:
			place, (lat, lng) = g.geocode(toGeo)
			a = "%s: %.5f, %.5f" % (place, lat, lng)
			marker = re.sub(',', ';', a)
			f.write(marker + ' ')
		except ValueError:
			print "Error Too many markers!"
			try:
				f.write("Too many markers for " + toGeo)
			except UnicodeEncodeError:
				f.write("Too many markers - name not unicode")
				continue
			continue
			
		# wait a moment so the geocoding doesn't get over run
		print "Waiting"
		time.sleep(2)
		
	
	f.write('\n')

# Done getting data! Close file.
f.close()