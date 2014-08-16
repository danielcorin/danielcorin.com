from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'siteproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', TemplateView.as_view(template_name='home.html'), name="home"),
    url(r'^apps/$', TemplateView.as_view(template_name='apps.html'), name="apps"),
    url(r'^curses/$', 'nocurses.views.curses_view', name="curses"),
    url(r'^hud/$', 'selfhud.views.hud_view', name="hud"),
)