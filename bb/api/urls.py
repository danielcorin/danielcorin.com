from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from tastypie.api import Api
from resources import EntryResource, UserResource
v1_api = Api(api_name='v1')
v1_api.register(EntryResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
	# backbone test app: oh life clone
    url(r'^$', TemplateView.as_view(template_name='bb/app.html'), name=""),
    url(r'^req/$', TemplateView.as_view(template_name='bb/req.html'), name=""),

    url(r'^api/', include(v1_api.urls)),
)