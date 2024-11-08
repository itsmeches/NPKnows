from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ImageModel  # Importing the custom ImageModel defined in models.py

# Unregister the default User admin to allow for customization
admin.site.unregister(User)

# Define a custom UserAdmin class to manage User model behavior
class CustomUserAdmin(UserAdmin):
    # You can specify custom fields or behaviors for the User admin panel here
    # This example keeps the default UserAdmin functionality
    pass

# Register the User model with the custom UserAdmin class
admin.site.register(User, CustomUserAdmin)

# Register the ImageModel with a customized admin interface
@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    # Fields to display on the main admin page for ImageModel
    list_display = ('uuid', 'image', 'user', 'prediction_result', 'created_at', 'updated_at', 'status')
    
    # Filters to allow quick sorting of ImageModel entries based on certain fields
    list_filter = ('status', 'created_at')
    
    # Enable search functionality on specific fields for easy data lookup
    search_fields = ('uuid', 'user__username', 'prediction_result')
    
    # Additional customizations can be added here, such as custom actions or further layout modifications
