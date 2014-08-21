from django.shortcuts import render
from django.http import HttpResponse
import json
import sys
import dateutil.parser
import datetime
import time
from datetime import timedelta
import os
import selfhud.update
from django.conf import settings
from unqlite import UnQLite

def localize_time(dt):
	return dt - timedelta(hours=7)

def hud_view(request):
	db_name = 'selfhud/apis.db'
	db = UnQLite(db_name)
	hud = json.loads(db['apis'])
	convert_times(hud)
	return render(request, 'hud.html', hud)

def localize(d, key="", loc=True):
	if loc:
		d[key] = localize_time(dateutil.parser.parse(d[key]))
	else:
		d[key] = dateutil.parser.parse(d[key])

def convert_times(d):
	localize(d['github'], key='created_at')
	try:
		localize(d['lastfm'], key='date')
	except KeyError:
		pass
	localize(d['twitter'], key='date')
	localize(d['strava'], loc=False, key='start_date')
	localize(d['goodreads'], key='updated_at')
	for b in d['goodreads']['currently_reading']:
		localize(b, key='started_at')
	localize(d['untappd'], key='created_at')
	d['trakt']['movie_watched'] = localize_time(datetime.datetime.fromtimestamp(d['trakt']['episode_watched']))
	d['trakt']['episode_watched'] = localize_time(datetime.datetime.fromtimestamp(d['trakt']['episode_watched']))
	d['kippt']['created'] = datetime.datetime.fromtimestamp(d['kippt']['created'])

def api_json_view(request):
	# db_name = os.path.join(settings.STATIC_ROOT, 'apis.db')
	# if db_name not in os.listdir(os.getcwd()):
	# 	selfhud.update.main()
	# with f as open(db_name, 'r')
	# hud = json.loads(f.read())
	db_name = 'selfhud/apis.db'
	db = UnQLite(db_name)
	hud = json.loads(db['apis'])
	return HttpResponse(json.dumps(hud), content_type="application/json")