from django.apps import AppConfig

# Define the configuration for the 'api' application
class ApiConfig(AppConfig):
    # Specify the type of auto field to use for automatically generated primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Set the name of the app; it should match the directory name of the app
    name = 'api'
