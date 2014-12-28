from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Entry(models.Model):
	user = models.ForeignKey(User)
	entry = models.TextField()
	created = models.DateTimeField()
	date = models.DateField()

	def __unicode__(self):
		return "%s" % (self.date)

	class Meta:
		verbose_name_plural = "entries"