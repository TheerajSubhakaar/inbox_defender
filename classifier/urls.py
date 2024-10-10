# classifier/urls.py

from django.urls import path
from classifier import views  # Import views instead of a specific function

urlpatterns = [
    path('', views.classify_message, name='classify_message'),  # Access the function via the module
]
