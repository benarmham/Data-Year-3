import urllib2 
from bs4 import BeautifulSoup
from geopy import geocoders
import re
import time

file = open('/Users/benarmham/Desktop/iucncodetry/iucn-data2.txt', 'w')

# use species ID to create a url
url = "http://www.iucnredlist.org/details/106003380/0"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
			
# scrape location fields from html
locations = soup.find_all(attrs={"class":"group"})
eachLoc = soup.find(attrs={"class":"group"}) 
for eachLoc in locations:
	l = eachLoc.get_text(" ", strip=True)
	location = l + ';'
	
	# find type of location (native, possibly extinct, etc)
	loc = re.findall('^(.*?):', location)
	for string in loc:
		description = string
		print description + ':description - ok'
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
	
	#write a final comma
	file.write(',')
	
# start a new line in the txt ready for the loop to go again
file.write('\n')

# done getting data! Close file.
file.close()