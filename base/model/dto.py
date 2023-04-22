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

class PropertyPhotoDto:
	url : str

	def __init__(self, url):
		self.url = url

class PropertyPhotoSerializer(serializers.Serializer):
	url = serializers.CharField(max_length=100)

class PropertyDto:
	id : int
	country : str
	city : str
	address : str
	exchange : str
	price : float
	square_feet : int
	rooms : int
	type : str
	name : str
	photos : []

	def __init__(self, id, country, city, address, exchange, price, square_feet, rooms, type, name, photos):
		self.id = id
		self.country = country
		self.city = city
		self.address = address
		self.exchange = exchange
		self.price = price
		self.square_feet = square_feet
		self.rooms = rooms
		self.type = type
		self.photos = photos
		self.name = name

class PropertySerializer(serializers.Serializer):
	id = serializers.IntegerField()
	country = serializers.CharField()
	city = serializers.CharField()
	address = serializers.CharField()
	exchange = serializers.CharField()
	price = serializers.DecimalField(max_digits=10, decimal_places=2)
	square_feet = serializers.IntegerField()
	rooms = serializers.IntegerField()
	type = serializers.CharField()
	name = serializers.CharField()
	photos = PropertyPhotoSerializer(many=True)

class UserProfileDto:
	first_name : str
	last_name : str
	email : str
	favorites : PropertyDto

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



