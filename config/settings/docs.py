import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_PAGINATION_LIMIT = 10

SECRET_KEY = 's5r+!fpsl*@^@v%ki3x3zjs4%mi&9=4e31%126s($5fj&y!@u2'
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'twitter',
    'twitter.users.apps.UsersAppConfig',
    'twitter.tweets.apps.TweetsConfig',
]
