from django.shortcuts import render
from jsondb import jsondb
import json
import sys
import dateutil.parser
import datetime
import time
from datetime import timedelta
import os
import selfhud.update

def localize_time(dt):
	return dt - timedelta(hours=7)

def hud_view(request):
	db_name = 'apis.db'
	if db_name not in os.listdir(os.getcwd()):
		selfhud.update.main()
	db = jsondb(db_name)
	hud = db.data
	convert_times(hud)
	return render(request, 'hud.html', hud)

def localize(d, key="", loc=True):
	if loc:
		d[key] = localize_time(dateutil.parser.parse(d[key]))
	else:
		d[key] = dateutil.parser.parse(d[key])

def convert_times(d):
	localize(d['github'], key='created_at')
	localize(d['lastfm'], key='date')
	localize(d['twitter'], key='date')
	localize(d['strava'], loc=False, key='start_date')
	localize(d['goodreads'], key='updated_at')
	for b in d['goodreads']['currently_reading']:
		localize(b, key='started_at')
	localize(d['untappd'], key='created_at')
	d['trakt']['movie_watched'] = localize_time(datetime.datetime.fromtimestamp(d['trakt']['episode_watched']))
	d['trakt']['episode_watched'] = localize_time(datetime.datetime.fromtimestamp(d['trakt']['episode_watched']))
	d['kippt']['created'] = datetime.datetime.fromtimestamp(d['kippt']['created'])