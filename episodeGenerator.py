import random, requests, bs4, logging, re

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

def requester(season):
	logging.debug('Creating URL for season %s...' % season)

	# IMDb identifier for the show - Default: It's Always Sunny in Philladelphia
	
	showID = 'tt0472954'
	showUrl = 'https://www.imdb.com/title/' + showID + '/episodes?season='
	seasonUrl = showUrl + str(season)
	res = requests.get(seasonUrl)
	res.raise_for_status()
	episodes = bs4.BeautifulSoup(res.text, 'html.parser')
	return episodes

def randomNum(maxNum=12):
	
	# For now number of seasons is hardcoded.
	
	logging.debug('Generating random number between 1 and %s...' % maxNum)
	num = random.randint(1,maxNum)
	return num

def maxEps(episodes):
	logging.debug('Requesting data for season %s...' % season)
	try:
		epsNum = episodes.select('meta[itemprop="episodeNumber"]')
		logging.debug('%s episodes found.' % len(epsNum))
		return len(epsNum)
	except:
		logging.debug('Failed to retrieve number of episodes.')
		return 99

def episodeData(bsObject, episode):
	episodeId = 'ref_=ttep_ep%s' % episode
	try:
		episodeObject = bsObject.find_all(href=re.compile(episodeId))
		return episodeObject
	except:
		logging.debug('Failed to find episode data.')
		return 0

def episodeTitle(episodeData):
	try:
		logging.debug('Successfully retrieved episode title.')
		title = episodeData[1].get('title')
		return title
	except:
		logging.debug('No match - returning generic could\'ve-been-title.')
		return placeholderEpisodes[random.randint(1,len(placeholderEpisodes))-1]


def episodeDesc(episodeData):
	try:
		descriptionObject = episodeData[1].find_parent().find_next_sibling(class_='item_description').string
		logging.debug('Successfully retrieved description.')
		description = str(descriptionObject).strip('\n').strip(' ')
		return description
	except:
		logging.debug('Failed to retrieve description.')
		return 'N/A'

placeholderEpisodes = 	['Frank goes to Hollywood',
						'The Gang goes South', 
						'Mac and Dennis get a pet', 
						'Mac goes to Hell',
						'The Gang battles Climate Change',
						'Sweet Dee makes the News',
						'The Gang eats an Elephant',
						'The Gang fights for their Right to Party']

print('Random Philly!')

season = randomNum()
episodes = requester(season)
episodeNum = randomNum(maxEps(episodes))
episodeInfo = episodeData(episodes, episodeNum)
episodeName = episodeTitle(episodeInfo)
episodeDescription = episodeDesc(episodeInfo)

print('Season #%s - Episode #%s' % (season, episodeNum))
print(episodeName)
print(episodeDescription)
