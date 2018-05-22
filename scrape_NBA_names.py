from selenium import webdriver
from bs4 import BeautifulSoup
import time

class Player():
	def __init__(self):
		self.name = ""
		self.link = ""
		self.pos = ""
		self.dim = ""

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
player_height_weight = nba_players.find_all('div', class_ = 'nba-player-index__details')

# p = player_names_links[1]
# print p['title']
# print p['href']

j = 0
addLink = 'http://www.nba.com'
for i in player_names_links:
	newPlay = Player()
	indiv = player_height_weight[j]
	span = indiv.find_all('span')
	corrLink = addLink + i['href']
	newPlay.link = corrLink
	newPlay.name = i['title']
	newPlay.pos = span[0].text
	newPlay.dim = span[1].text
	player_list.append(newPlay)
	j = j+1

for one_player in player_list:
	print one_player.name
	print one_player.pos
	print one_player.dim
	print one_player.link

driver.quit()
