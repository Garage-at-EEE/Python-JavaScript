'''
This program is for personal use
to record the NBA after game feelings 
will need web scrap to use the date and game info
create local files .docx
may use bootstrap to make it advanced.
'''
schedual=dict(zip([x%13 for x in range (10,20) if x%13 != 0],
[
'https://www.basketball-reference.com/leagues/NBA_2018_games.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-november.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-december.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-january.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-february.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-march.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-april.html']
))# create  a dictionary for urls.

Urls = [
'https://www.basketball-reference.com/leagues/NBA_2018_games.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-november.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-december.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-january.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-february.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-march.html',
'https://www.basketball-reference.com/leagues/NBA_2018_games-april.html']

# team_board=['Celtics', 'Cavaliers', 'Rockets', 'Warriors', 'Bucks', 'Hawks', 'Mavericks', 'Hornets', 'Pistons', 'Nets', 'Pacers', 'Pelicans', 'Grizzlies', 'Heat', 'Magic', 'Blazers', 'Suns', 'Kings', 'Timberwolves', 'Spurs', 'Nuggets', 'Jazz', '76ers', 'Wizards', 'Clippers', 'Lakers', 'Knicks', 'Thunder', 'Bulls', 'Raptors']
team = 'Boston Celtics'

import time
import urllib.request
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

count = 1
local_time = time.asctime(time.localtime())
UTC_time = time.asctime(time.gmtime())
timex = [x for x in UTC_time.split(' ')]
timey = [timex[i] for i in [1,2,-1]]
strt = '{} {}, {}'.format(*timey)

def Create(info):
	global count
	soup = BeautifulSoup(info,'html.parser')
	for item in soup.findAll('tr')[1:]:
		information = [data.text for data in item.findAll('td')]
		if team in '\n'.join(information):
			if team.split(' ')[1] in information[3]:
				opponent = information[1]
				place = 'Home'
			else:
				opponent = information[3]
				place = 'Guest'
			game_time = item.find('th').text[5:]
			if game_time[5]==',':
				game_time = game_time[:4]+'0'+game_time[4:]	
				count+=1
				print(game_time+'\n')
				print(place+'\n')
				print(f'{team} {information[(information.index(team)+1)]} vs {information[(information.index(opponent)+1)]} {opponent}\n')
				print('------------------------------------------------------')

for item in Urls:
	sauce = urllib.request.urlopen(item)
	info = sauce.read()
	Create(info)
	sauce.close()