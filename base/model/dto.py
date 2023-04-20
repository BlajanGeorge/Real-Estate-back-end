from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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