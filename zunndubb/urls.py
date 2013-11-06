from django.conf.urls import patterns, include, url
from django.conf import settings
from class_based_auth_views.views import LoginView, LogoutView

from django.contrib import admin
admin.autodiscover()

from zunndubb.views import HomeView

urlpatterns = patterns('',
    #url(r'^auth/', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^movies/', include('apps.movies.urls')),
    url(r'^wishlist/', include('apps.wishlist.urls')),
    url(r'^groups/', include('apps.groups.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^~', include('apps.profiles.urls')),
    # url(r'^social/', include('social_auth.urls' )),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', HomeView.as_view(), name='home'),
)


# Static file handling for dev env
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )



# Autoload template tags see AUTOLOAD_TEMPLATETAGS in settings
if hasattr(settings, 'AUTOLOAD_TEMPLATETAGS'):
    from django.template.loader import add_to_builtins
    for tag in settings.AUTOLOAD_TEMPLATETAGS:
        add_to_builtins(tag)

