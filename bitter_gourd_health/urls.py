"""
URL configuration for bitter_gourd_health project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# project/urls.py
from django.contrib import admin
from django.urls import path, include  # 'include' is imported for future usage if needed
from api.views import ImageView, UserRegistrationView, LoginView  # Update to use LoginView




# project/urls.py
from django.contrib import admin
from django.urls import path
from api.views import ImageView, UserRegistrationView, LoginView  # Ensure you have the correct imports

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Endpoint for image upload and prediction
    path('api/image/', ImageView.as_view(), name='image_view'),  
    
    # Optional: If you want a separate endpoint for prediction only
    # If both 'image/' and 'predict/' serve the same purpose, consider removing one
    path('api/predict/', ImageView.as_view(), name='predict_view'),  
    
    # User registration and login endpoints
    path('api/register/', UserRegistrationView.as_view(), name='register'),  
    path('api/login/', LoginView.as_view(), name='login'),  
]

