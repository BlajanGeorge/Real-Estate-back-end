import jwt
from rest_framework.exceptions import ParseError
from django.conf import settings
from base.models import *


class JWTAuthentication:
	def get_the_token_from_header(self, token):
		token = token.replace('Bearer', '').replace(' ', '')
		return token

	def authenticate(self, request, roles, request_user_id):
		jwt_token = request.headers.get('Authorization')
		if jwt_token is None:
			return False
		jwt_token = self.get_the_token_from_header(jwt_token)

		try:
			payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
		except jwt.exceptions.InvalidSignatureError:
			print('Invalid signature')
			return False
		except jwt.exceptions.ExpiredSignatureError:
			print('Signature has expired')
			return False
		except jwt.exceptions.DecodeError:
			return False

		user_id = payload.get('user_id')
		user = User.objects.filter(id=user_id).first()

		if user is None:
			return False

		if request_user_id is not None and user.role != 'AGENT':
			if int(user_id) != int(request_user_id):
				return False

		if user.role not in roles:
			return False

		return True