from django.apps import AppConfig


class ThemeConfig(AppConfig):
    name = 'theme'

    def ready(self):
        # Makes sure all signal handlers are connected
        from theme import handlers
