import urllib2
import re
from bs4 import BeautifulSoup
from geopy import geocoders

url = "http://www.iucnredlist.org/details/42657/0"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
locations = soup.find(attrs={"class":"group"}).get_text(" ", strip=True)
location = locations + ';'
print location

markers = re.findall('\s(.*?);', location)
for string in markers:
	a = string
	print a
	toGeo = a.split(',', 1)[0]
	g = geocoders.Google()
	place, (lat, lng) = g.geocode(toGeo)
	marker = "%s: %.5f, %.5f" % (place, lat, lng)
	print marker