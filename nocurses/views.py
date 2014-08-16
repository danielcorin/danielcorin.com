from django.shortcuts import render
from django.http import HttpResponse
from models import Curse

import json

DANNY="DC"
DES="DD"
AMT_PER_CURSE = 0.25

def calculate_amount(count):
	return AMT_PER_CURSE*count

def curses_view(request):
	if request.POST:
		c = Curse(name=request.POST.get('name'))
		c.save()

	danny = Curse.objects.filter(name=DANNY)
	des = Curse.objects.filter(name=DES)

	count_danny = len(danny)
	count_des = len(des)

	amt_danny = "%.2f" % (calculate_amount(count_danny))
	amt_des = "%.2f" % (calculate_amount(count_des))
	resp = {
		"count_danny": count_danny,
		"count_des": count_des,
		"amt_danny": amt_danny,
		"amt_des": amt_des,
	}
	if request.POST:
		return HttpResponse(json.dumps(resp), content_type="application/json")
	else:
		resp["recent_danny"] = danny.order_by('date').reverse().first()
		resp["recent_des"] = des.order_by('date').reverse().first()
		return render(request, 'curses.html', resp)

