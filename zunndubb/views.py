from django.views.generic import TemplateView
from apps.movies.models import Movie

class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['leader_movies'] = Movie.objects.all()[:10]
        return context
