from django.apps import AppConfig


class BusConfig(AppConfig):
    name = 'bus'

    def ready(self):
        """シグナルを読み込む"""
        import bus.signals
