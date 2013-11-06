from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    #url(r'^get_torrents/(?P<movie>[a-zA-Z0-9_%.,\s)(]+)/$', GetTorrentsView.as_view(), name='movie_torrents'),
    url(r'^get_torrents/(?P<movie>[\w\s\W\S]+)/$', GetTorrentsView.as_view(), name='movie_torrents'),
    url(r'^(?P<imdb_id>tt\d+)/$', MovieDetailView.as_view(), name='movie_detail'),
    url(r'^$', MovieListView.as_view(), name='movie_list'),
)

