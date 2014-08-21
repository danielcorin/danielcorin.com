import auth
import requests
from requests_oauthlib import OAuth1
import urllib
import xml.etree.ElementTree as ET
import datetime
from django.conf import settings
import os
import json
from unqlite import UnQLite

def github():
	user = auth.github['user']
	url = "https://api.github.com/users/%s/events" % (user)
	event_type = auth.github['event_type']

	r = requests.get(url=url)
	data = r.json()

	item = None
	for i in data:
		if i['type'] == "PushEvent":
			item = i
			break
			
	payload = item['payload']
	repo = item['repo']
	
	# newest commit is last in the list
	commit = payload['commits'][-1]
	repo_name = repo['name']
	user = item['actor']['login']
	# created_at = localize_time(dateutil.parser.parse(item['created_at']))
	created_at = item['created_at']
	url_template = "https://github.com/%s"
	user_url = url_template % user
	repo_url = url_template % repo_name

	return {
		"commit_message":commit['message'],
		"user":user,
		"repo_name":repo_name,
		"created_at":created_at,
		"user_url":user_url,
		"repo_url":repo_url,
	}

def last_fm():
	api_key = auth.lastfm['api_key']
	client_secret = auth.lastfm['client_secret']
	user = auth.lastfm['user']

	url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&format=json" % (user, api_key)

	r = requests.get(url=url)
	data = r.json()
	date = None
	track = data['recenttracks']['track'][0]
	title = track['name']
	artist = track['artist']['#text']
	status = "No status"
	if '@attr' in track:
		if track['@attr']['nowplaying'] == "true":
			status = "Now playing"
	else:
		date = track['date']['#text']
		# date = localize_time(dateutil.parser.parse(date))
		status = "Played at:"
	url = track['url']
	user_url = "http://www.last.fm/user/%s" % (user)

	info = {
		"title":title,
		"artist":artist,
		"status":status,
		"url":url,
		"user_url":user_url,
	}
	if date:
		info['date'] = date

	return info

def twitter():
	CONSUMER_KEY = auth.twitter['consumer_key']
	CONSUMER_SECRET = auth.twitter['consumer_secret']
	OAUTH_TOKEN = auth.twitter['oauth_token']
	OAUTH_TOKEN_SECRET = auth.twitter['oauth_token_secret']
	USER = auth.twitter['user']


	def get_oauth():
		oauth = OAuth1(CONSUMER_KEY,
			client_secret=CONSUMER_SECRET,
			resource_owner_key=OAUTH_TOKEN,
			resource_owner_secret=OAUTH_TOKEN_SECRET)
		return oauth

	def get_tweets(oauth=None, timeline="home", count=20):
		if not oauth:
			oauth = get_oauth()
		url = "https://api.twitter.com/1.1/statuses/%s.json?count=%d" % (timeline, count)
		r = requests.get(url=url, auth=oauth)
		data = r.json()
		return data
	tweets = get_tweets(oauth=get_oauth(), timeline="user_timeline", count=1)
	last_tweet = tweets[0]
	urls = []
	try:
		media = last_tweet['extended_entities']['media']
		urls = []
		for m in media:
			try:
				urls.append(m['url'])
			except:
				pass
	except KeyError:
		pass
	text = last_tweet['text']
	# date = localize_time(dateutil.parser.parse(last_tweet['created_at']))
	date = last_tweet['created_at']

	tweet_id = last_tweet['id']
	tweet_url = "https://twitter.com/%s/status/%d" % (USER, tweet_id)
	user_url = "https://twitter.com/%s" % USER
	info =  {
		"text":text,
		"date":date,
		"tweet_url":tweet_url,
		"user_url":user_url,
	}
	return info

def strava():
	CLIENT_ID = auth.strava['client_id']
	CLIENT_SECRET = auth.strava['client_secret']
	ACCESS_TOKEN = auth.strava['access_token']
	ATHLETE_ID = auth.strava['athlete_id']

	M_TO_MI = 0.00062
	M_TO_FT = 3.28
	MPS_TO_MPH = 2.23


	ath_url = ('https://www.strava.com/api/v3/athlete/activities/')
	header = {'Authorization': ('Bearer %s' % ACCESS_TOKEN)}

	data = requests.get(ath_url, headers=header).json()[0]
	name = data['name']
	# start_date = dateutil.parser.parse(data['start_date_local'])
	start_date = data['start_date_local']
	elevation_gain = data['total_elevation_gain']*M_TO_FT
	distance = data['distance']*M_TO_MI
	max_speed = data['max_speed']*MPS_TO_MPH
	elapsed_time = datetime.timedelta(seconds=data['elapsed_time'])
	activity_type = data['type']
	activity_url = "http://www.strava.com/activities/%s" % data['id']
	athlete_url = "http://www.strava.com/athletes/%d" % (ATHLETE_ID)

	return {
		"name":name,
		"start_date":start_date,
		"distance_in_mi":"%.1f" %distance,
		"max_speed_mph":"%.1f" %max_speed,
		"elevation_gain_ft":"%.1f" %elevation_gain,
		"elapsed_time":str(elapsed_time),
		"activity_type":activity_type,
		"activity_url":activity_url,
		"athlete_url":athlete_url,
	}

def get_root(url):
	tree = ET.parse(urllib.urlopen(url))
	return tree.getroot()

def goodreads():
	KEY = auth.goodreads['key']
	SECRET_KEY = auth.goodreads['secret_key']
	USER_ID = auth.goodreads['user_id']

	# get most recent status
	status_url = "https://www.goodreads.com/user/show/%d.xml?key=%s" % (USER_ID, KEY)
	r = get_root(status_url)
	update = r.find('user').find('updates').find('update')
	action_text = update.find('action_text').text
	action_text = "Danny %s" % action_text
	# updated_at = localize_time(dateutil.parser.parse(update.find('updated_at').text))
	updated_at = update.find('updated_at').text

	# get books in currently-reading list
	url = "https://www.goodreads.com/review/list/%d.xml?key=%s&v=2&shelf=currently-reading"
	url = url  % (USER_ID, KEY)
	currently_reading = []
	root = get_root(url)
	reviews = root.find('reviews')

	for review in reviews.findall('review'):
		book = review.find('book')
		title = book.find('title').text
		link = book.find('link').text
		author = book.find('authors').find('author').find('name').text
		started_at = review.find('started_at').text
		currently_reading.append({
			"title":title,
			"author":author,
			"started_at":started_at,
			"link":link,
		})

	info = {
		"user_url": "https://www.goodreads.com/review/list/%d" % (USER_ID),
		"currently_reading":currently_reading,
		"action_text":action_text,
		"updated_at":updated_at,
	}
	if not currently_reading:
		info['status'] = "None"
	return info

def trakt():
	USERNAME = auth.trakt['username']
	API_KEY = auth.trakt['api_key']

	user_url = "https://trakt.tv/user/%s" % USERNAME
	movie_url = "http://api.trakt.tv/user/library/movies/watched.json/%s/%s" %(API_KEY, USERNAME)
	show_url = "http://api.trakt.tv/user/library/shows/watched.json/%s/%s" % (API_KEY, USERNAME)

	r = requests.get(url=movie_url)
	movie_data = r.json()
	r = requests.get(url=show_url)
	show_data = r.json()

	# get viewing times of most recent movie and episode
	activity_url = "http://api.trakt.tv/user/lastactivity.json/%s/%s" % (API_KEY, USERNAME)
	r = requests.get(url=activity_url)
	activity_data = r.json()

	# movie_watched = localize_time(datetime.datetime.fromtimestamp(activity_data['movie']['watched']))
	# episode_watched = localize_time(datetime.datetime.fromtimestamp(activity_data['episode']['watched']))
	movie_watched = activity_data['movie']['watched']
	episode_watched = activity_data['episode']['watched']
	# get info for most recently viewed movie and show
	movie = movie_data[0]
	show = show_data[0]

	movie_url = movie['url']
	show_url = show['url']

	season = show['seasons'][0]['season']
	episode = show['seasons'][0]['episodes'][0]
	episode_url = "%s/season/%d/episode/%d" % (show_url, season, episode)
	episode_string = "%dx%d" % (season, episode)

	return {
		"user_url":user_url,
		"movie_title":movie['title'],
		"movie_url":movie_url,
		"show_title":show['title'],
		"show_url":show_url,
		"episode_url":episode_url,
		"episode_string":episode_string,
		"movie_watched":movie_watched,
		"episode_watched":episode_watched,
	}

def kippt():
	USERNAME = auth.kippt['username']
	base_url = "https://kippt.com"
	user_url = "%s/%s" % (base_url, USERNAME)
	url = "%s/api/users/%s/clips" % (base_url, USERNAME)

	data = requests.get(url=url)
	clips = data.json()

	clip = clips['objects'][0]

	return {
		"clip_url":clip['url'],
		"clip_title":clip['title'],
		"user_url":user_url,
		"created":clip['created'],
	}

def untappd():
	USERNAME = auth.untappd['username']
	CLIENT_ID = auth.untappd['client_id']
	CLIENT_SECRET = auth.untappd['client_secret']
	user_url = "https://untappd.com/user/%s" % (USERNAME)

	url = "http://api.untappd.com/v4/user/checkins/%s?client_id=%s&client_secret=%s" % (USERNAME, CLIENT_ID, CLIENT_SECRET)
	r = requests.get(url=url)
	data = r.json()

	last_checkin = data['response']['checkins']['items'][0]
	# created_at = localize_time(dateutil.parser.parse(last_checkin['created_at']))
	created_at = last_checkin['created_at']
	rating_score = last_checkin['rating_score']
	beer_name = last_checkin['beer']['beer_name']
	brewery_name = last_checkin['brewery']['brewery_name']
	brewery_url = last_checkin['brewery']['contact']['url']

	return {
		"created_at":created_at,
		"rating_score":rating_score,
		"beer_name":beer_name,
		"brewery_name":brewery_name,
		"user_url":user_url,
		"brewery_url":brewery_url,
	}

def add_api(hud, name, func):
	try:
		hud[name] = func()
	except:
		print func()
		pass

def main():
	hud = {}
	add_api(hud, "github", github)
	add_api(hud, "lastfm", last_fm)
	add_api(hud, "twitter", twitter)
	add_api(hud, "strava", strava)
	add_api(hud, "goodreads", goodreads)
	add_api(hud, "trakt", trakt)
	add_api(hud, "kippt", kippt)
	add_api(hud, "untappd", untappd)
	db_name = 'apis.db'
	db = UnQLite(db_name)
	db['apis'] = json.dumps(hud)
	db.close()


if __name__ == '__main__':
	main()
