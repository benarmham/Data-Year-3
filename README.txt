/INTRODUCTION/

This is my repository full of the code I have used in scraping the IUCN Red List 
to create the hunted map at benhamilton.co.uk/hunted.html 
as well as the html code of that map.
It is primarily to demonstrate my work as part of my final 
University project looking at Data Journalism.


/CONTENTS/

IUCN Scrape
- 	Twelve versions of my RedPanda python scraping code, as well as five smaller tests 
	that were used to scrape to the IUCN Red List.

Initial Data
-	Contains the downloaded XML file which is required to carry out the scrape.
	The information has been downloaded from this Red List search:
			http://www.iucnredlist.org/search/link/513b4bbd-c3e5cf4d

Final Data
-	Contains the final finished product of the RedPanda python scrape (iucn-data.txt)
	and two examples of cleaner data as CSV's, refined in Google Refine.
	
IUCN Master
-	A complete list of all the CSV tables created in Numbers to create the final table 
	(IUCN Data-CartoJS.csv) that counts the totals to be used in the CartoDB map.

Hunted Vis
-	Contains the html for the Hunted map, as well as the two css style sheets downloaded
	from the CartoDB tutorials website, and edited to suit my visualisation.


/OTHER LINKS/

The Distribute python package needed to install other download packages:
	https://pypi.python.org/pypi/distribute/

BeautifulSoup 4 needed to parse the species data from the IUCN Red List website:
	http://www.crummy.com/software/BeautifulSoup/bs4/download/
	

/FORKED REPOSITORIES/

Geopy and Pip have both been forked from their Github pages - both were used in the 
RedPanda Python scrape