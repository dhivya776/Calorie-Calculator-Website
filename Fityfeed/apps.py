from django.apps import AppConfig


class FityfeedConfig(AppConfig):
    name = 'Fityfeed'

    def ready(self):
        import Fityfeed.cron

    