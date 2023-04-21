from django.urls import path
from . import views

urlpatterns = [
path('locations', views.validLocations),
path('users', views.users),
path('login', views.login),
path('users/<user_id>', views.user_by_id),
path('users/<user_id>/profile', views.user_by_id_profile),
path('users/<user_id>/password', views.user_by_id_password),
path('users/<user_id>/favorites', views.user_by_id_favorites),
]