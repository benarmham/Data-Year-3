import urllib2
import re
from bs4 import BeautifulSoup
url = "http://www.iucnredlist.org/details/714/0"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)
locations = soup.find(attrs={"class":"group"}).get_text(" ", strip=True)
location = locations + ';'
print location

native = re.search("Native:", location)
marker = location[:native.start()] + location[native.end():]
print marker