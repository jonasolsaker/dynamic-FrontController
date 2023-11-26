from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer

# can be moved into utils.py in app
import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from db_connection import db

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = db.user_trial.find_one({'username': username})
    if user and check_password(password, user['password']):
        token = jwt.encode({'username': user['username']}, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token})
    return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
def logout(request):
    return Response({})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = serializer.data
        response_data.pop('password', None)  # Ensures password is not included in the response
        return Response(response_data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def test_token(request):
    auth_header = request.headers.get('Authorization', None)
    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                return Response({'status': 'Token is valid', 'username': payload['username']})
            except jwt.ExpiredSignatureError:
                return Response({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                return Response({'error': 'Invalid Token'}, status=401)
        else:
            return Response({'error': 'Invalid Authorization header format'}, status=400)
    return Response({'error': 'No token provided'}, status=400)