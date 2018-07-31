from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "twitter.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import user.signals  # noqa F401
        except ImportError:
            pass
