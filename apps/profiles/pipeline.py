from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from social.pipeline.partial import partial
import urllib2


def check_email(strategy, details, user, response, *args, **kwargs):
    backend_name = strategy.backend.name
    if user:
        return
    else:
        if details['email']:
            return
        if strategy.session.get('saved_email'):
            details['email'] = strategy.session.get('saved_email')
            return
        else:
            return redirect('/~fill_email/?next=%s' % backend_name)