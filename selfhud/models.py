from django.db import models
from datetime import datetime
from django.utils import timezone

class APIData(models.Model):
	api_string = models.TextField()
	date = models.DateTimeField()
	
	def save(self):
		self.date = datetime.utcnow().replace(tzinfo=timezone.utc)
		super(APIData, self).save()
	class Meta:
		verbose_name_plural = "API data"
