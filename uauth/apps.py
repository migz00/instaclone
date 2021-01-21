from django.apps import AppConfig


class UauthConfig(AppConfig):
    name = 'uauth'

    def ready(self):
        import uauth.signals
