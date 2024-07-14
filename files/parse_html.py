import json
import re
from bs4 import BeautifulSoup

def parseFromLink(link, outputArrName):

    with open(link, 'r', encoding='utf-8') as file:
        html_content = file.read()

    #Set up beautifulsoup and init array
    soup = BeautifulSoup(html_content, 'html.parser')

    #Find first g-scrolling-carousel, init artworks array to push to json
    carousel = soup.find('g-scrolling-carousel')
    artworks = []
    pattern = re.compile(r'\bklitem\b')

    #Each item in the carousel is in an <a> with the class 'klitem', let's iterate through those
    for painting in carousel.find_all('a', class_=pattern):
        #Split title parameter that contains both the title and the year of the painting
        title = painting['title'].split('(')
        name = title[0].strip()

        #Handle there not always being more elements after split
        if len(title) > 1: 
            extensions = [title[1].strip(')')]
        else:
            extensions = []

        #Append like to google address to match expected-array
        link = "https://www.google.com" + painting['href'] 

        #How can I defer finding the img until the page has rendered, using selenium?
        #Maybe ruby does this better....
        imgTag = painting.find('img')
        if imgTag:
            img = imgTag.get('data-key', imgTag.get('src'))
        else:
            img = None

        #Build dictionary and append it to artworks array
        artwork = {}
        artwork['name'] = name
        #Extensions is not always present
        if extensions:
            artwork['extensions'] = extensions
        artwork['link'] = link
        artwork['image'] = img

        artworks.append(artwork)

    #Output similar to expected-array, ensure all chars render
    output = json.dumps({outputArrName: artworks}, ensure_ascii=False, indent=2)

    with open('files/output-array.json', 'w',) as file:
        file.write(output)


####RESOURCES####
#https://realpython.com/beautiful-soup-web-scraper-python/
#https://realpython.com/python-json/
#https://regex-generator.olafneumann.org/