# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
import scraperwiki
from bs4 import BeautifulSoup
import string
import unicodedata
import time

headers = ["Name","Department","Total Ratings","Overall Quality","Easiness","Hot"]
#Dictionary of school ids (keys) that map to tuple of school name and number of pages
colleges = {"580":("MIT",16),"1222":("Yale",23),"181":("CMU",28), "1085":("UChicago",28),"1040":("Tufts",46), "1350":("Duke",84),"1255":("UTexas",84),"953":("Stanford",32),"799":("Rice",17),"780":("Princeton",16)}

for sid in colleges.keys():
    college,pages = colleges[sid]
    print college
    for i in xrange(1,pages+1):
        response = scraperwiki.scrape("http://www.ratemyprofessors.com/SelectTeacher.jsp?sid=%s&pageNo=%s" % (sid,str(i)))
        time.sleep(5)
        soup = BeautifulSoup(response)
        rows = soup.find_all("div",{"class":"entry odd vertical-center"})
        rows.extend(soup.find_all("div",{"class":"entry even vertical-center"}))
        for row in rows:
            columns = row.find_all('div')
            columns = columns[3:]
            variables = {}
            for i,col in enumerate(columns):
                value = unicodedata.normalize('NFKD', col.text).encode('ascii', 'ignore')
                variables[headers[i]] = value
            variables["College"] = college
            scraperwiki.sqlite.save(unique_keys=['Name',"Department"], data = variables)
    
