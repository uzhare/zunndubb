from django.db import models
from apps.movies.models import Movie
from django.conf import settings


class HaveManager(models.Manager):
    def get_query_set(self):
        return super(HaveManager, self).get_query_set().filter(status=Wish.WISH_HAVE)

class WantManager(models.Manager):
    def get_query_set(self):
        return super(WantManager, self).get_query_set().filter(status=Wish.WISH_WANT)

class InProgressManager(models.Manager):
    def get_query_set(self):
        return super(InProgressManager, self).get_query_set().filter(status=Wish.WISH_IN_PROGRESS)

class Wish(models.Model):
    WISH_HAVE = 'have_it'
    WISH_WANT = 'want_it'
    WISH_IN_PROGRESS = 'in_progress'
    WISH_DONT_CARE = 'dont_care'
    WISH_TYPES = (
        (WISH_WANT, 'Want'),
        (WISH_HAVE, 'Have'),
        (WISH_IN_PROGRESS, 'In Progress'),
        (WISH_DONT_CARE, 'Don\'t Care'),
    )
    movie = models.ForeignKey(Movie, related_name='wishes')
    status = models.CharField(max_length=8, choices=WISH_TYPES)
    profile = models.ForeignKey(settings.AUTH_USER_MODEL)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    have = HaveManager()
    want = WantManager()
    in_progress = InProgressManager()

    class Meta:
        verbose_name_plural = 'wishes'
        db_table = 'wishlist'
        unique_together = ('movie', 'profile')

    def __unicode__(self):
        output = "%s %s %s"
        if self.status == Wish.WISH_HAVE:
            output = output % (self.profile, 'has', self.movie)
        elif self.status == Wish.WISH_WANT:
            output = output % (self.profile, 'wants', self.movie)
        elif self.status == Wish.WISH_IN_PROGRESS:
            output = output % (self.profile, 'is downloading', self.movie)
        elif self.status == Wish.WISH_DONT_CARE:
            output = output % (self.profile, 'doesn\'t care about', self.movie)

        return output


