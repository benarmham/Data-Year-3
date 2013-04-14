# import all the stuff/tools we need 
import urllib2 
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from geopy import geocoders
import re
import time

# open our txt file for the data to go in
f = open('/Users/benarmham/Desktop/iucncodetry/iucn-data2.txt', 'w')

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
					f.write(names + '; ')
				except UnicodeEncodeError:
					print 'Name not Unicode' 
					f.write('Common name not unicode' + '; ')

	# find assessment category
	for assessment in species.findall('assessment'):
		cat = assessment.find('category').text
		print cat + ': cat - ok'
		f.write(',' + cat + ',')
	
	# and the species id, scientific names, and class
	speciesID = species.get('id')
	sciName = species.find('scientific_name').text
	sciClass = species.find('class_name').text
	print speciesID + ': ID - ok'
	print sciName + ': scientific name - ok'
	print sciClass + ': class - ok'
	f.write(speciesID + ',' + sciName + ',' + sciClass + ',')
	
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
	while True:
		try:
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
				f.write(description + ',')
	
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
					
					print "Getting geodata for " + toGeo
		
					# start geocoding, allowing for extra marker errors and name errors
					g = geocoders.Google()
					try:
						place, (lat, lng) = g.geocode(toGeo)
						latlon = "%s: %.5f, %.5f" % (place, lat, lng)
						marker = re.sub(',', ';', latlon)
						f.write(marker + ' ')
					except ValueError:
						print 'Error Too many markers! '
						try:
							f.write("Too many markers for " + toGeo + ' ')
						except UnicodeEncodeError:
							f.write('Too many markers - name not unicode ')
							continue
						continue
			
					# wait a moment so the geocoding doesn't get over run
					print "Waiting"
					time.sleep(2)
		
		# connection timeout exception
		except urllib2.URLError:
			print 'URL error, retrying'
			continue
		break

	# start a new line in the txt ready for the loop to go again
	f.write('\n')

# done getting data! Close file.
f.close()