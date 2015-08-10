from django.apps import AppConfig


class CNHProfileConfig(AppConfig):
    name = 'cnh_profile'
    verbose_name = 'Copy N Haste Profile'

    def ready(self):
        import handlers
