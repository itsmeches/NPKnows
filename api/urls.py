# api/urls.py
from django.urls import path
from .views import ImageView, UserRegistrationView, LoginView  # Import views directly from api app

urlpatterns = [
    path('image/', ImageView.as_view(), name='image_view'),
    path('predict/', ImageView.as_view(), name='predict_view'),  # Optional alias if needed
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]    
