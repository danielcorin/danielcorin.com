from django.contrib.auth.models import User

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from bb.models import Entry
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie import fields


class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		# fields = ['username', 'first_name', 'last_name', 'last_login']
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		filtering = {
            'username': ALL,
        }


class EntryResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')

	class Meta:
		queryset = Entry.objects.all()
		allowed_methods = ['get', 'post', 'put', 'delete']
		resource_name = 'entry'
		authorization = Authorization()
		filtering = {
			'user': ALL_WITH_RELATIONS,
			'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
		}
