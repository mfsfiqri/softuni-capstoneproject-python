from django.apps import AppConfig


class AkunConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogCapstoneProject.akun'

    def ready(self):
        import blogCapstoneProject.akun.signals
