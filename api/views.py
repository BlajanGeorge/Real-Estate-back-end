from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
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
	print(user_id)
	return Response()




