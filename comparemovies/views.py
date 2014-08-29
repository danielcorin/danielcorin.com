from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import auth
from django.template import Context, Template

table_item_id = 0

def query_rt(movie_title):
	rt_api_key = auth.rt_api_key
	url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=%s&q=%s&page_limit=5" % (rt_api_key, movie_title)
	r = requests.get(url)
	response = r.json()
	data = {}

	for m in response['movies']:
		if m['title'].lower() == movie_title.lower():
			data['movie'] = m
			data['success'] = True
			break
	else:
		try:
			data['movie'] = response['movies'][0]
		except:
			data['success'] = False
	return data

def query_imdb(movie_title):
	# url = "http://mymovieapi.com/?title=%s&type=json&plot=simple&episode=1&limit=1&yg=0&mt=none&lang=en-US&offset=&aka=simple&release=simple&business=0&tech=0" % (movie_title)
	url = "http://www.omdbapi.com/?i=&t=%s" % (movie_title)
	r = requests.get(url)
	response = r.json()

	if 'Response' in response and response['Response'] == "False":
		response['success'] = False
	else:
		response['success'] = True
	return response


def query(request):
	movie_title = request.POST['movie']
	rt_data = query_rt(movie_title)
	movie_title = rt_data['movie']['title']
	imdb_data = query_imdb(movie_title)
	if rt_data['success'] and imdb_data['success']:
		global table_item_id
		data = {
			"rt_data":rt_data,
			"imdb_data":imdb_data,
			"id":table_item_id,
		}
		data['link'] = "http://www.rottentomatoes.com/m/%s" % (movie_title.lower().replace(" ","_"))
		table_item_id += 1
		return render(request, 'comparemovies/table-item.html', data)
	else:
		return HttpResponse(json.dumps({
			"message":"Film not found",
			"success":False,
		}), content_type="application/json")

def recent(request):
	API_KEY = auth.rt_api_key
	url = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/in_theaters.json?apikey=%s" % (API_KEY)
	movies = {"movies": []}
	r = requests.get(url=url)
	movies['movies'] = [m['title'] for m in r.json()['movies']]
	return HttpResponse(json.dumps(movies))


