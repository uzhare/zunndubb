from .common import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': root('zunndubb.sqlite3'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS += (
    'social.apps.django_app.default',
    'crispy_forms',
    'imagekit',
    'apps.paginator',
    'apps.movies',
    'apps.profiles',
    'apps.wishlist',
    'apps.groups',
)

AUTOLOAD_TEMPLATETAGS += (
)


AUTHENTICATION_BACKENDS += (
    'social.backends.google.GoogleOpenId',    
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.facebook.FacebookAppOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)


SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/' 

SOCIAL_AUTH_TWITTER_KEY = 'd1tWTQEr1P7vYx31HWIQ'
SOCIAL_AUTH_TWITTER_SECRET = 'FQIAgQRJav8OUS89TqWQk6DcqZNUKHdzxWmsjAknYg'

SOCIAL_AUTH_FACEBOOK_KEY =    '331148946992859'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b72b038cd01aa41a6161218427bc5e82'

SOCIAL_AUTH_GOOGLE_KEY = '491340407013.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_SECRET = 'L_pjbue8WmOn7jOIsMA9lmnN'


SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.partial.save_status_to_session',
    'apps.profiles.pipeline.check_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
AUTH_USER_MODEL = 'profiles.Profile'
