from django.urls import path
from .views import ImageView, UserRegistrationView, LoginView, arduino_data, validate_token, leaf_view, get_recommendation

# Define URL patterns for the API endpoints
urlpatterns = [
    # Optional endpoint for making predictions on images (aliasing to the same view as 'image_view')
    path('predict/', ImageView.as_view(), name='predict_view'),
    # Endpoint for user registration
    path('register/', UserRegistrationView.as_view(), name='register'),
    # Endpoint for user login
    path('login/', LoginView.as_view(), name='login'),
    # Correct the URL path for the arduino_data endpoint
    path('arduino/', arduino_data, name='arduino_data'),
    path('validate-token/', validate_token, name='validate-token'),
    path('leaf/', leaf_view, name='leaf'),
    path('recommendation/', get_recommendation, name='get_recommendation'),
]
