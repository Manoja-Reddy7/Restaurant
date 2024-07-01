from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    # we are using the below funtion to work the signals file fine.
    def ready(self):
        import accounts.signals
