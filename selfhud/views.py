from django.shortcuts import render
from django.http import HttpResponse
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
			hud = call_update()
			apis.delete()
		else:
			hud = json.loads(apis.api_string)
			convert_times(hud)
	else:
		hud = call_update()
	hud['load_time'] = "%.2f seconds" % (time.time() - start_time)
	return render(request, 'hud.html', hud)

def localize_time(dt):
	return dt - timedelta(hours=7)

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
	d['trakt']['episode_watched'] = localize_time(datetime.datetime.fromtimestamp(d['trakt']['episode_watched']))
	d['kippt']['created'] = datetime.datetime.fromtimestamp(d['kippt']['created'])


def get_hud_api(request, api_name):
	if api_name == 'github':
		data = update.github()
		# data['created_at'] = localize_time(dateutil.parser.parse(data['created_at']))
	elif api_name == 'goodreads':
		data = update.goodreads()
	elif api_name == 'kippt':
		data = update.kippt()
	elif api_name == 'lastfm':
		data = update.lastfm()
	elif api_name == 'strava':
		data = update.strava()
	elif api_name == 'trakt':
		data = update.trakt()
	elif api_name == 'twitter':
		data = update.twitter()
	elif api_name == 'untappd':
		data = update.untappd()
	elif api_name == 'swarm':
		data = update.swarm()
	else:
		data = {"message":"error"}
	return HttpResponse(json.dumps(data), content_type="application/json")


