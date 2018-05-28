from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

class Player():
	def __init__(self):
		self.name = ""
		self.link = ""
		# self.pos = ""
		# self.dim = ""

player_list = []

driver = webdriver.PhantomJS(executable_path = r'C:\Users\sarim\Desktop\Scraper\phantomjs.exe')
driver.get('http://www.nba.com/players')
pause = 0
lastHeight = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight

html_doc = driver.page_source
soup = BeautifulSoup(html_doc, 'lxml')

nba_players = soup.find('section', class_ = 'row nba-player-index__row')
player_names_links = nba_players.find_all('a', class_ = None)
# player_height_weight = nba_players.find_all('div', class_ = 'nba-player-index__details')

# p = player_names_links[1]
# print p['title']
# print p['href']
addLink = 'http://www.nba.com'
#visit only the first two links. Remove the scope to visit all the links and download
#the stats for each player. This will take significant time and processing, so be wary.
for i in player_names_links[0:2]:
	newPlay = Player()
	corrLink = addLink + i['href']
	newPlay.link = corrLink
	newPlay.name = i['title']
	player_list.append(newPlay)


# for one_player in player_list:
# 	print one_player.name
# 	print one_player.pos
# 	print one_player.dim
# 	print one_player.link

def get_detail_all_players(player_list):

	driver = webdriver.PhantomJS(executable_path = r'C:\Users\sarim\Desktop\Scraper\phantomjs.exe')

	for p in player_list:
		url = p.link
		driver.get(url)
		soup = BeautifulSoup(driver.page_source, 'lxml')

		h_section = soup.find('section', class_ = 'nba-player-vitals__top-left small-6')
		h_p = h_section.find('p', class_ = 'nba-player-vitals__top-info-metric')
		height = h_p.text
		height = height.replace('/', '')
		height = ''.join(height.split())
		p.height = height

		w_section = soup.find('section', class_ = 'nba-player-vitals__top-right small-6')
		w_p = w_section.find('p', class_ = 'nba-player-vitals__top-info-metric')
		weight = w_p.text
		weight = weight.replace('/', '')
		weight = ''.join(weight.split())
		p.weight = weight

		stat_section = soup.find('section', class_ = 'nba-player-season-career-stats')
		header_stat = stat_section.find('th', text = 'CAREER STATS')
		mpg = header_stat.find_next_sibling('td')
		p.mpg = mpg.renderContents()
		fg = mpg.find_next_sibling('td')
		p.fg = fg.renderContents()
		threeP = fg.find_next_sibling('td')
		p.threeP = threeP.renderContents()
		ft = threeP.find_next_sibling('td')
		p.ft = ft.renderContents()
		ppg = ft.find_next_sibling('td')
		p.ppg = ppg.renderContents()
		rpg = ppg.find_next_sibling('td')
		p.rpg = rpg.renderContents()
		apg = rpg.find_next_sibling('td')
		p.apg = apg.renderContents() 
		bpg = apg.find_next_sibling('td')
		p.bpg = bpg.renderContents()

	return player_list
	driver.quit()

player_list_big = get_detail_all_players(player_list)

#print the first two entries
for player in player_list_big:
	print('name:' + player.name)
	print('height:' + player.height)
	print('weight:' + player.weight)
	print('~~STATS~~')
	print('MPG:' + player.mpg)
	print('FG%:' + player.fg)
	print('3P%:' + player.threeP)
	print('FT%:' + player.ft)
	print('PPG:' + player.ppg)
	print('RPG:' + player.rpg)
	print('APG:' + player.apg)
	print('BPG:' + player.bpg)
driver.quit()
