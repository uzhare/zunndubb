from django.views.generic import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from braces.views import AjaxResponseMixin
import requests
from .models import Movie


class MovieListView(ListView):
    model = Movie
    paginate_by = 20
    context_object_name = 'movie_list'


class MovieDetailView(DetailView):
    model = Movie
    slug_field = 'imdb_id'
    slug_url_kwarg = 'imdb_id'

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        context['profile_is_downloading'] = self.request.user.is_downloading(context['movie'])
        context['profile_has_it'] = self.request.user.has_it(context['movie'])
        context['profile_wants_it'] = self.request.user.wants_it(context['movie'])
        context['profile_doesnt_care'] = self.request.user.doesnt_care(context['movie'])
        return context

class GetTorrentsView(AjaxResponseMixin, TemplateView):
    template_name = 'movies/partials/torrents.html'

    def get_context_data(self, *args, **kwargs):
        context = super(GetTorrentsView, self).get_context_data(*args, **kwargs)
        r = requests.get('http://apify.ifc0nfig.com/tpb/search?id=%s' % self.kwargs.get('movie'))
        context['torrents'] = r.json
        return context

