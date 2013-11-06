import os
from datetime import datetime
from glob import glob
from django.core.management.base import BaseCommand, CommandError
from django.core.files.images import ImageFile
import json
from apps.movies.models import Movie, Attribute


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        movies = glob('data/IMDB250/*.json')

        for movie in movies:
            self.stdout.write('=' * 40)
            imdbid, ext = os.path.splitext(os.path.basename(movie))
            metadata = json.load(open(movie, 'r'))
            poster = ImageFile(open('data/IMDB250/%s.jpg' % imdbid))

            movie = Movie()
            movie.title = metadata.get('title', None)
            movie.imdb_id = imdbid
            movie.poster = poster
            movie.rating = float(metadata.get('rating', 0.0))
            movie.plot= metadata.get('plot', 'Plot not available...')
            movie.rated = metadata.get('rated', '')
            movie.year = int(metadata.get('year', 0))
            movie.type = metadata.get('type', None)
            self.stdout.write('    %s (%s)' % (movie.title, movie.year))

            # Calculate release date.
            release_date = metadata.get('release_date', None)
            if release_date is not None:
                release_date = str(release_date)
                year  = int(release_date[:4])
                month = int(release_date[4:6])
                day   = int(release_date[6:8])
                if day > 0 and year > 0 and month > 0:
                    release_date = datetime.strptime(str(release_date), '%Y%m%d')
                else:
                    release_date = None
            movie.release_date = release_date
            self.stdout.write('    Release Date: %s' % release_date)

            movie.save()

            # Set attributes
            for ns in ['genres', 'actors', 'directors', 'language', 'also_known_as']:
                if ns.startswith('also_'):
                    key = 'alt_titles'
                elif ns.startswith('lang'):
                    key = 'language'
                else:
                    key = ns[:-1]

                self.stdout.write('    Attribute: %s' % ns)
                for val in metadata.get(ns, []):

                    attr, is_new = Attribute.objects.get_or_create(
                            namespace = key,
                               value = val
                           )
                    self.stdout.write('        %s' % val)
                    movie.attributes.add(attr)

                movie.save
