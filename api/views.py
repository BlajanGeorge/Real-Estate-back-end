from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q,F,ExpressionWrapper
import sys
sys.path.insert(0,"..")

from base.models import *
from base.serializers import *
from base.model.dto import *
from base.security.security import *
from django.core import serializers
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import models
import time
import datetime

@api_view(['GET'])
def validLocations(request):
	countries = []
	cities = []

	for c in ValidCountry :
		countries.append({'name' : c.value})
	for c in ValidCity:
		cities.append({'name' : c.value, 'country' : c.label})


	return Response(LocationDtoSerializer(LocationDto(countries, cities)).data)


@api_view(['GET', 'POST'])
def users(request):
	if request.method == 'POST':
		try:
			if request.data.get('agent_token').strip():
			    if request.data.get('agent_token') == settings.AGENT_TOKEN:
			    	return saveUser(request, Role.AGENT.value)
			    else :
			        return Response(status=status.HTTP_401_UNAUTHORIZED)
			else :
				return saveUser(request, Role.CUSTOMER.value)
		except AttributeError :
			return Response(status=status.HTTP_400_BAD_REQUEST)

	if request.method == 'GET':
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data)

def saveUser(request, role : str):
	payload = request.data
	payload['role'] = role
	payload.pop('agent_token')

	serializer = UserSerializer(data=payload)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	else :
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
	try:
		user = User.objects.filter(email=request.data.get('email')).first()
		if user is None:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		if user.password != request.data.get('password'):
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		return Response(LoginResponseSerializer(LoginResponse(user.id, user.role, MyTokenObtainPairSerializer.get_token(user).access_token)).data)
	except AttributeError:
		return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_by_id(request, user_id):
	if JWTAuthentication().authenticate(request, ['AGENT', 'CUSTOMER'], user_id) == False:
		return Response(status=status.HTTP_401_UNAUTHORIZED)
	user = User.objects.filter(id=user_id).first()
	if user is None:
		return Response(status=status.HTTP_404_NOT_FOUND)

	favorites = []

	for fav in user.favorites.all():
		photos = []
		for photo in fav.propertyphoto_set.all():
			photos.append(PropertyPhotoDto(photo.url))
		favorites.append(PropertyDto(fav.id, fav.country, fav.city, fav.address, fav.exchange, fav.price, fav.square_feet, fav.rooms, fav.type, fav.name, photos))

	user_profile = UserProfileDto(user.first_name, user.last_name, user.email, favorites)
	return Response(UserProfileSerializer(user_profile).data)

@api_view(['PATCH'])
def user_by_id_profile(request, user_id):
	if JWTAuthentication().authenticate(request, ['AGENT', 'CUSTOMER'], user_id) == False:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	user = User.objects.filter(id=user_id).first()
	if user is None:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user.last_name = request.data.get('last_name')
	user.first_name = request.data.get('first_name')
	user.save()

	serializer = UserSerializer(user, many=False)
	if serializer.is_valid:
		return Response(serializer.data)
	
	return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def user_by_id_password(request, user_id):
	if JWTAuthentication().authenticate(request, ['AGENT', 'CUSTOMER'], user_id) == False:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	user = User.objects.filter(id=user_id).first()
	if user is None:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if user.password != request.data.get('current_password'):
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	user.password = request.data.get('new_password')
	user.save()

	serializer = UserSerializer(user, many=False)
	if serializer.is_valid:
		return Response(serializer.data)
	
	return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST', 'DELETE'])
def user_by_id_favorites(request, user_id):
	if JWTAuthentication().authenticate(request, ['AGENT', 'CUSTOMER'], user_id) == False:
		return Response(status=status.HTTP_401_UNAUTHORIZED)


	user = User.objects.filter(id=user_id).first()

	if user is None:
		return Response(status=status.HTTP_404_NOT_FOUND)

	favorites = []

	if request.method == 'GET':
		return Response(display_favorites(user.favorites.all()).data)

	if request.method == 'DELETE':
		prop_id = request.GET.get('property_id')

		if prop_id is None:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		user.favorites.through.objects.filter(property_id=prop_id).delete()
		return Response(display_favorites(user.favorites.all()).data)

	if request.method == 'POST':
		prop_id = request.data.get('property_id')

		if prop_id is None:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		property = Property.objects.filter(id=prop_id).first()

		if property is None:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		user.favorites.add(property)
		return Response(display_favorites(user.favorites.all()).data)


	return Response(status=status.HTTP_400_BAD_REQUEST)


def display_favorites(fav_db):
	favorites = []
	for fav in fav_db:
		photos = []
		for photo in fav.propertyphoto_set.all():
			photos.append(PropertyPhotoDto(photo.url))
		favorites.append(PropertyDto(fav.id, fav.country, fav.city, fav.address, fav.exchange, fav.price, fav.square_feet, fav.rooms, fav.type, fav.name, photos))

	serializer = PropertySerializer(favorites, many=True)
	return serializer


@api_view(['GET'])
def properties(request):
	if JWTAuthentication().authenticate(request, ['AGENT', 'CUSTOMER'], None) == False:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	properties = Property.objects.all()

	properties_response = []

	for property in properties:
		photos = []
		for photo in property.propertyphoto_set.all():
			photos.append(PropertyPhotoDto(photo.url))
		properties_response.append(PropertyDto(property.id, property.country, property.city, property.address, property.exchange, property.price, property.square_feet, property.rooms, property.type, property.name, photos))

	serializer = PropertySerializer(properties_response, many=True)

	return Response(serializer.data)

@api_view(['GET'])
def properties_with_filter(request):
	if JWTAuthentication().authenticate(request, ['AGENT', 'CUSTOMER'], None) == False:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	type = request.GET.get('type')
	rooms = request.GET.get('rooms')
	min_sq = request.GET.get('min_sq')
	max_sq = request.GET.get('max_sq')
	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')

	types = []

	if type == 'All' :
		types = ['House', 'Apartment']
	else:
		types.append(type)

	query = None

	if type is not None:
		query = Q(type__in=types)

	if rooms is not None:
		if query is None:
			query = Q(rooms=rooms)
		else:
			query = query & Q(rooms=rooms)

	if min_sq is not None:
		if query is None:
			query = Q(square_feet__gte=min_sq)
		else:
			query = query & Q(square_feet__gte=min_sq)

	if max_sq is not None:
		if query is None:
			query = Q(square_feet__lte=max_sq)
		else:
			query = query & Q(square_feet__lte=max_sq)

	if min_price is not None:
		if query is None:
			query = Q(price__gte=min_price)
		else:
			query = query & Q(price__gte=min_price)

	if max_price is not None:
		if query is None:
			query = Q(price__lte=max_price)
		else:
			query = query & Q(price__lte=max_price)

	if query is not None:
		properties = Property.objects.filter(query)
	else:
		properties = Property.objects.all()

	properties_response = []

	for property in properties:
		photos = []
		for photo in property.propertyphoto_set.all():
			photos.append(PropertyPhotoDto(photo.url))
		properties_response.append(PropertyDto(property.id, property.country, property.city, property.address, property.exchange, property.price, property.square_feet, property.rooms, property.type, property.name, photos))

	serializer = PropertySerializer(properties_response, many=True)

	return Response(serializer.data)

@api_view(['GET'])
def property_by_id(request, property_id) :
	if JWTAuthentication().authenticate(request, ['AGENT', 'CUSTOMER'], None) == False:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	if property_id is None:
		return Response(status=status.HTTP_400_BAD_REQUEST)

	property = Property.objects.filter(id=property_id).first()

	if property is None:
		return Response(status=status.HTTP_404_NOT_FOUND)

	photos = []

	for photo in property.propertyphoto_set.all():
		photos.append(PropertyPhotoDto(photo.url))

	property_response = PropertyDto(property.id, property.country, property.city, property.address, property.exchange, property.price, property.square_feet, property.rooms, property.type, property.name, photos)

	serializer = PropertySerializer(property_response, many=False)

	return Response(serializer.data)

@api_view(['GET', 'POST', 'DELETE'])
def user_by_id_schedules(request, user_id):
	if JWTAuthentication().authenticate(request, ['AGENT', 'CUSTOMER'], None) == False:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	if request.method == 'POST':
		property_id = request.GET.get('property_id')
		date = request.data.get('date')

		if property_id is None or date is None:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		if current_milli_time() + 86400000 > int(date):
			return Response("Schedule must be at least one day ahead", status=status.HTTP_400_BAD_REQUEST)

		ocuppied = Schedule.objects.annotate(end_date=ExpressionWrapper(F('date') + 3600000, output_field=models.BigIntegerField())).filter(Q(property_id=property_id, date__lt=date, end_date__gt=date) | Q(date=date)).first()

		if ocuppied is not None:
			start_search_date = ocuppied.date
			found = False

			while found == False:
				start_search_date += 3600000
				test = Schedule.objects.annotate(end_date=ExpressionWrapper(F('date') + 3600000, output_field=models.BigIntegerField())).filter(Q(property_id=property_id, date__lt=start_search_date, end_date__gt=start_search_date) | Q(date=start_search_date)).first()
				if test is None:
					found = True

			return Response('Another schedule is programmed in this interval, most appropiate time of the choosed one is {}'.format(datetime.datetime.fromtimestamp(( start_search_date + 10800000)/1000.0)), status=status.HTTP_400_BAD_REQUEST)

		Schedule.objects.create(property_id=property_id, user_id=user_id, date=date)

		return Response('Schedule created with success')


	return Response()

def current_milli_time():
    return round(time.time() * 1000)


@api_view(['GET'])
def property_by_id_schedules(request, property_id):
	if JWTAuthentication().authenticate(request, ['AGENT', 'CUSTOMER'], None) == False:
		return Response(status=status.HTTP_401_UNAUTHORIZED)

	if property_id is None:
		return Response(status=status.HTTP_400_BAD_REQUEST)


	schedules = Schedule.objects.filter(property_id=property_id).all()

	schedules_resp = []

	for schedule in schedules:
		user = User.objects.filter(id=schedule.user.id).first()
		schedules_resp.append(ScheduleDto(schedule.id, user.id, user.first_name, user.last_name, schedule.date))

	serializer = ScheduleSerializer(schedules_resp, many=True)

	return Response(serializer.data)
