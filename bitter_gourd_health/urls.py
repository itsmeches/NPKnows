"""
URL configuration for bitter_gourd_health project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
Function views:
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views:
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf:
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Import necessary modules
from django.contrib import admin
from django.urls import path, include  # 'include' is imported for future usage if needed
from api.views import ImageView, UserRegistrationView, LoginView  # Import views to handle requests

# URL routing configuration
urlpatterns = [
    # Admin interface route
    path('admin/', admin.site.urls),  # Admin interface available at /admin/

    # API routes
    path('api/', include('api.urls')),  # Include the API app's URLs under the /api/ path prefix

    # User registration route
    path('api/register/', UserRegistrationView.as_view(), name='register'),  # Registration view

    # User login route
    path('api/login/', LoginView.as_view(), name='login'),  # Login view for user authentication

    # Image upload and prediction route
    path('api/image/', ImageView.as_view(), name='image_view'),  # View for image upload and processing

    # Alternative prediction route
    path('api/predict/', ImageView.as_view(), name='predict_view'),  # Another route for prediction (optional)
]
