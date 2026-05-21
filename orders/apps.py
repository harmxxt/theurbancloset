from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    # No signals import — invoice generation is called
    # directly from views.py after items are created.
