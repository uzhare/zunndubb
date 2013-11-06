from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^wish/(?P<imdb_id>tt\d+)/(?P<wish>\w+)/$', WishView.as_view(), name='wish'),
)

