'''

This module is for web scraping on wikipedia;
it will scrape the title and the content larger than 250 characters and will end at the first period after the 250th character.

'''

import bs4
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

def wiki(url):
	file = urlopen(url)
	page = file.read()
	file.close()
	soup = BeautifulSoup(page, "html.parser")
	for tag in soup.find_all('sup'):
		tag.replaceWith('')
	for tag in soup.find_all('table'):
		tag.replaceWith('')
	full_text=''
	h1_header = soup.find('h1')
	h2_header = soup.find('h2')
	for p in h1_header.find_all_next('p'):
		if p in h2_header.find_all_previous('p'):
			text = p.text.encode('ascii','ignore').decode('ascii')
			full_text+=text
		if text != '':
			full_text+='\n'
	text_part = full_text[:250]
	for item in full_text[250:]:
		text_part+=item
		if item == '.':
			break
	return str(text_part)

# read only the title of the wikipedia document
def wiki_title(url):
	file = urlopen(url)
	page = file.read()
	file.close()
	soup = BeautifulSoup(page, "html.parser")
	x=soup.find('h1',{'id':'firstHeading'}).text
	return str(x)

if __name__ == '__main__':
	result = wiki('https://en.wikipedia.org/wiki/Python_(programming_language)')
	print(result)