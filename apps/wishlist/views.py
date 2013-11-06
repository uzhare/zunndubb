from django.views.generic import View
from django.shortcuts import get_object_or_404
from braces.views import AjaxResponseMixin, JSONResponseMixin, LoginRequiredMixin
from apps.movies.models import Movie
from .models import Wish

class WishView(JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin, View):

    def get_context_data(self, **kwargs):
        context = super(WishView, self).get_context_data(**kwargs)
        return context

    def get(self, *args, **kwargs):
        movie = get_object_or_404(Movie, imdb_id=self.kwargs['imdb_id'])
        wish, is_new = Wish.objects.get_or_create(
                            movie=movie,
                            profile=self.request.user,
                        )
        wish.status = self.kwargs['wish']
        wish.save()
        import time
        message = 'Noted!'
        return self.render_json_response({
            'success': True,
            'message': message,
        })

