from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ImageModel  # Import your ImageModel

# Unregister the default User admin
admin.site.unregister(User)

# Register the User model with a custom UserAdmin
class CustomUserAdmin(UserAdmin):
    # Define your custom fields and behavior here
    pass

admin.site.register(User, CustomUserAdmin)

# Register ImageModel in the admin
@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'image', 'user', 'prediction_result', 'created_at', 'updated_at', 'status')  # Include all relevant fields
    list_filter = ('status', 'created_at')  # Optional: add filters for better navigation
    search_fields = ('uuid', 'user__username', 'prediction_result')  # Optional: add search functionality

    # Optionally, you can add custom actions or modify the admin interface further
