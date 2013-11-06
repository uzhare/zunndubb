from datetime import datetime
from urlparse import urlparse
from django.db import models
from django.db.models import Q
from django_extensions.db.fields.json import JSONField
from django.core.urlresolvers import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize, ResizeToFill, Adjust


import requests
from PIL import Image
from StringIO import StringIO
from django.core.files.images import ImageFile

class Attribute(models.Model):
    NS_ACTOR = 'actor'
    NS_DIRECTOR = 'director'
    NS_LANGUAGE = 'language'
    NS_GENRE = 'genre'
    NS_ALT_TITLE= 'alt_titles'
    NS_CHOICES = (
        (NS_ACTOR, 'Actor'),
        (NS_DIRECTOR, 'Director'),
        (NS_LANGUAGE, 'Language'),
        (NS_GENRE, 'Genre'),
        (NS_ALT_TITLE, 'Alternate Title'),
    )

    namespace = models.CharField(max_length=128, choices=NS_CHOICES)
    value = models.CharField(max_length=512)

    class Meta:
        db_table = 'attributes'

    def __unicode__(self):
        return '%s:%s' % (self.namespace, self.value)


class MovieInProgressManager(models.Manager):
    def get_query_set(self):
        return super(MovieInProgressManager, self)\
                   .get_query_set()\
                   .filter(progress=Movie.PROGRESS_IN_PROGRESS)


class MovieCompleteManager(models.Manager):
    def get_query_set(self):
        return super(MovieCompleteManager, self)\
                   .get_query_set()\
                   .filter(progress=Movie.PROGRESS_COMPLETE)

class MovieNotStartedManager(models.Manager):
    def get_query_set(self):
        return super(MovieNotStartedManager, self)\
                   .get_query_set()\
                   .filter(progress=Movie.PROGRESS_NOT_STARTED)

class Movie(models.Model):
    TV_SERIES_TYPE = 'TVS'
    MOVIE_TYPE = 'M'
    TV_MOVIE_TYPE = 'TV'
    VIDEO_TYPE = 'V'
    VIDEO_GAME_TYPE = 'VG'
    TYPE_CHOICES = (
        (MOVIE_TYPE, 'Movie'),
        (TV_SERIES_TYPE, 'TV Series'),
        (TV_MOVIE_TYPE, 'TV Movie'),
        (VIDEO_TYPE, 'Video'),
        (VIDEO_GAME_TYPE, 'Video Game')
    )
    PROGRESS_IN_PROGRESS = 'in progress'
    PROGRESS_COMPLETE = 'complete'
    PROGRESS_NOT_STARTED = 'not started'
    PROGRESS_CHOICES = (
        (PROGRESS_IN_PROGRESS, 'In Progress'),
        (PROGRESS_NOT_STARTED, 'Not Started'),
        (PROGRESS_COMPLETE, 'Complete'),
    )

    title = models.CharField(max_length=512)
    imdb_id = models.CharField(max_length=16)
    rating = models.FloatField()
    plot = models.TextField()
    rated = models.CharField(max_length=8)
    #poster = models.URLField()
    poster = models.ImageField(upload_to='posters', default='posters/default.jpg')
    poster_large = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            SmartResize(240, 320)], image_field='poster',
            format='JPEG', options={'quality': 90})
    poster_medium = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            SmartResize(180, 240)], image_field='poster',
            format='JPEG', options={'quality': 90})
    poster_mini = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
            SmartResize(100, 120)], image_field='poster',
            format='JPEG', options={'quality': 90})
    year = models.PositiveSmallIntegerField()
    type =  models.CharField(max_length=16, choices=TYPE_CHOICES)
    release_date = models.DateField(blank=True, null=True)
    attributes = models.ManyToManyField(Attribute)
    progress = models.CharField(max_length=16, choices=PROGRESS_CHOICES, default=PROGRESS_NOT_STARTED)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    in_progress = MovieInProgressManager()
    completed = MovieCompleteManager()
    not_started = MovieNotStartedManager()


    class Meta:
        db_table = 'movies'
        ordering = ('-rating',)
        get_latest_by = 'modified'

    def __unicode__(self):
        if self.release_date:
            return '%s (%s)' % (self.title, self.release_date.year)
        else:
            return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', args=[str(self.imdb_id)])

    def similar(self, num=8):
        # TODO: Find a better more scalable solution [MN]
        genres = self.genres
        return Movie.objects.filter(attributes__value__in=genres).exclude(pk=self.pk).distinct()[:num]

    @property
    def who_is_downloading(self):
        return self.wishes.filter(status='in_progress')

    @property
    def who_wants(self):
        return self.wishes.filter(status='want_it')

    @property
    def who_has(self):
        return self.wishes.filter(status='have_it')

    @property
    def who_doesnt_care(self):
        return self.wishes.filter(status='dont_care')

    @property
    def actors(self):
        return [item[0] for item in self.attributes.filter(namespace=Attribute.NS_ACTOR).values_list('value')[:10]]

    @property
    def directors(self):
        return [item[0] for item in self.attributes.filter(namespace=Attribute.NS_DIRECTOR).values_list('value')[:10]]

    @property
    def genres(self):
        return [item[0] for item in self.attributes.filter(namespace=Attribute.NS_GENRE).values_list('value')[:10]]

    @property
    def alt_titles(self):
        return [item[0] for item in self.attributes.filter(namespace=Attribute.NS_ALT_TITLE).values_list('value')[:10]]



