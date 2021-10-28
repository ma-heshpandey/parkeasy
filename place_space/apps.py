from django.apps import AppConfig


class PlaceSpaceConfig(AppConfig):
    name = 'place_space'

    def ready(self):
        from background_check import background_schedular
        background_schedular.start()