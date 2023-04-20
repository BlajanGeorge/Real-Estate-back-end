from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from base.models import *
from base.serializers import *

class LocationDto:
	countries : []
	cities : []

	def __init__(self, countries : [], cities : []):
		self.countries = countries
		self.cities = cities

class CountryDto:
	name : str
	phone_prefix : str

	def __init__(self, name : str, prefix : str):
		self.name = name
		self.phone_prefix = prefix

class CityDto:
	name : str
	country : str

	def __init__(self, name, country):
		self.name = name
		self.country = country

class CountryDtoSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=100)

class CityDtoSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=100)
	country = serializers.CharField(max_length=100)

class LocationDtoSerializer(serializers.Serializer):
	countries = CountryDtoSerializer(many=True)
	cities = CityDtoSerializer(many=True)

class LoginResponse:
	id : int
	role : str
	token : str

	def __init__(self, id, role, token):
		self.id = id
		self.role = role
		self.token = token

class LoginResponseSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	role = serializers.CharField(max_length=100)
	token = serializers.CharField(max_length=100)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.role
        # ...
        return token

class UserProfileDto:
	first_name : str
	last_name : str
	email : str
	favorites : Property

	def __init__(self, first_name, last_name, email, favorites):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.favorites = favorites


class UserProfileSerializer(serializers.Serializer):
	first_name = serializers.CharField(max_length=100)
	last_name = serializers.CharField(max_length=100)
	email = serializers.CharField(max_length=100)
	favorites = PropertySerializer(many=True)

	
