from django.urls import path
from . import views

urlpatterns = [
path('locations', views.validLocations),
path('users', views.users),
path('login', views.login),
path('users/<user_id>', views.user_by_id),
]