from django.shortcuts import render
# from django.http import HttpResponse
from models import APIData
import update
import json
import sys
import dateutil.parser
import datetime
from datetime import timedelta
from django.utils import timezone
import time
import os
import selfhud.update

def localize_time(dt):
	return dt - timedelta(hours=7)

def call_update():
	hud = update.main()
	a = APIData(api_string=json.dumps(hud))
	a.save()
	convert_times(hud)
	return hud

def hud_view(request):
	start_time = time.time()
	if len(APIData.objects.all()):
		apis = APIData.objects.all()[0]
		if datetime.datetime.utcnow().replace(tzinfo=timezone.utc) > (apis.date + timedelta(minutes=1)):
			apis.delete()
			hud = call_update()
		else:
			hud = json.loads(apis.api_string)
			convert_times(hud)
	else:
		hud = call_update()
	hud['load_time'] = "%.2f seconds" % (time.time() - start_time)
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