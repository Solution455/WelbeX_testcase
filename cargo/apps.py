from django.apps import AppConfig
from django.db import connection


class CargoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cargo'

    def ready(self):
        if 'cargo_location' in connection.introspection.table_names():
            from cargo.signals import load_data
            load_data()
