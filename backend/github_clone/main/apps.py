from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    def ready(self):
        from scheduler import scheduler
        print('READY')
        import websocket.signals
        # scheduler.start()
