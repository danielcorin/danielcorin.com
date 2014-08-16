from django.db import models
from datetime import datetime
from django.utils import timezone


class Curse(models.Model):
	name = models.CharField(max_length=120)

	DES = "DD"
	DANNY = "DC"
	ACTION_TYPE_CHOICES = (
		(DES, 'Des'),
		(DANNY, 'Danny'),
	)

	name = models.CharField(max_length=2, choices=ACTION_TYPE_CHOICES)
	date = models.DateTimeField()
	
	def save(self):
		self.date = datetime.utcnow().replace(tzinfo=timezone.utc)
		super(Curse, self).save()


	def __unicode__(self):
		return "%s: %s" % (self.name, self.date)
