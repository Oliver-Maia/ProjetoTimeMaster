from django.apps import AppConfig


class AgendaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "agenda"


    def ready(self):
        # Importa os signals
        import agenda.signals