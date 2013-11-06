from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^fill_email/$', FillEmailView.as_view(), name='fill_email'),
    url(r'^$', DashView.as_view(), name='dash'),
    url(r'^(?P<username>\w+)/$', ProfileView.as_view(), name='profile'),
    url(r'^settings/(?P<username>\w+)$', SettingsView.as_view(), name='settings'),
    #url(r'^(?P<email>[^@]+@[^@]+\.[^@]+)/$', ProfileView.as_view(), name='profile'),
)
