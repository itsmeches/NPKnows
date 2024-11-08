from django.urls import path
from .views import ImageView, UserRegistrationView, LoginView  # Import views from the api app

# Define URL patterns for the API endpoints
urlpatterns = [
    # Endpoint for handling image uploads and image-related actions
    path('image/', ImageView.as_view(), name='image_view'),
    
    # Optional endpoint for making predictions on images (aliasing to the same view as 'image_view')
    path('predict/', ImageView.as_view(), name='predict_view'),
    
    # Endpoint for user registration
    path('register/', UserRegistrationView.as_view(), name='register'),
    
    # Endpoint for user login
    path('login/', LoginView.as_view(), name='login'),
]
