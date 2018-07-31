from django.apps import AppConfig


class TweetsConfig(AppConfig):
    name = 'twitter.tweets'
    verbose_name = 'Tweets'

    def ready(self):
        """Override this to put in:
            Chat system checks
            Chat signal registration
        """
        try:
            import twitter.signals  # noqa F401
        except ImportError:
            pass
