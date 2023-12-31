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
path('properties', views.properties),
path('properties/filter', views.properties_with_filter),
path('properties/<property_id>', views.property_by_id),
path('users/<user_id>/schedules', views.user_by_id_schedules),
path('properties/<property_id>/schedules', views.property_by_id_schedules),
path('properties/<property_id>/schedules/count', views.property_by_id_schedules_count),
]