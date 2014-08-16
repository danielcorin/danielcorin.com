from __future__ import unicode_literals
from django.shortcuts import render
import auth
import requests
import json
import sys
from requests_oauthlib import OAuth1
import datetime
import urllib
import xml.etree.ElementTree as ET
import dateutil.parser

def hud_view(request):
	hud = {
		"github":github(),
		"lastfm":last_fm(),
		"twitter":twitter(),
		"strava":strava(),
		"goodreads":goodreads(),
	}
	return render(request, 'hud.html', hud)

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
	commit = payload['commits'][0]
	repo_name = repo['name']
	user = item['actor']['login']
	created_at = dateutil.parser.parse(item['created_at'])
	url_template = "https://github.com/%s"

	return {
		"commit_message":commit['message'],
		"user":user,
		"user":user,
		"repo_name":repo_name,
		"url_template":url_template,
		"created_at":created_at,
	}

def last_fm():
	api_key = auth.lastfm['api_key']
	client_secret = auth.lastfm['client_secret']
	user = auth.lastfm['user']

	url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&format=json" % (user, api_key)

	r = requests.get(url=url)
	data = r.json()
	track = data['recenttracks']['track'][0]
	title = track['name']
	artist = track['artist']['#text']
	date = dateutil.parser.parse(track['date']['#text'])
	url = track['url']

	return {
		"title":title,
		"artist":artist,
		"date":date,
		"url":url,
	}


def twitter():
	CONSUMER_KEY = auth.twitter['consumer_key']
	CONSUMER_SECRET = auth.twitter['consumer_secret']
	OAUTH_TOKEN = auth.twitter['oauth_token']
	OAUTH_TOKEN_SECRET = auth.twitter['oauth_token_secret']


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
	date = dateutil.parser.parse(last_tweet['created_at'])
	info =  {
		"text":text,
		"date":date,
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
	start_date = dateutil.parser.parse(data['start_date_local'])
	elevation_gain = data['total_elevation_gain']*M_TO_FT
	distance = data['distance']*M_TO_MI
	max_speed = data['max_speed']*MPS_TO_MPH
	elapsed_time = datetime.timedelta(seconds=data['elapsed_time'])
	activity_type = data['type']
	activity_url = "http://www.strava.com/activities/%s" % data['id']

	return {
		"name":name,
		"start_date":start_date,
		"distance_in_mi":"%.1f" %distance,
		"max_speed_mph":"%.1f" %max_speed,
		"elevation_gain_ft":"%.1f" %elevation_gain,
		"elapsed_time":str(elapsed_time),
		"activity_type":activity_type,
		"activity_url":activity_url,
	}

def goodreads():
	KEY = auth.goodreads['key']
	SECRET_KEY = auth.goodreads['secret_key']
	USER_ID = auth.goodreads['user_id']

	url = "https://www.goodreads.com/review/list/%d.xml?key=%s&v=2&shelf=currently-reading"
	url = url  % (USER_ID, KEY)

	currently_reading = []

	tree = ET.parse(urllib.urlopen(url))
	root = tree.getroot()

	reviews = root.find('reviews')

	for review in reviews.findall('review'):
		book = review.find('book')
		title = book.find('title').text
		author = book.find('authors').find('author').find('name').text
		started_at = dateutil.parser.parse(review.find('started_at').text)
		currently_reading.append({
			"title":title,
			"author":author,
			"started_at":started_at,
		})
	return currently_reading

