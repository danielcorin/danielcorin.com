from django.shortcuts import render
from models import Entry

def entry(request, year, month='0', day='0'):
	print year, month, day