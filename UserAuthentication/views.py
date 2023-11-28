from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from Subscription.views import add_location as add_location_subscription
from Subscription.serializers import LocationSerializer
from Subscription.helpers import geocode_location

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

@api_view(['POST'])
def add_location(request):
    username = request.data.get('username')
    location = request.data.get('location')
    user = db.user_trial.find_one({'username': username})
    if not username or not location:
        return Response({'error': 'Username and location are required'}, status=400)
    # Check if the location already exists in the user's locations
    if location in user.get('subscribed_locations', []):
        return Response({'error': 'Location already exists for this user'}, status=400)
     # Update the user's document by adding the location to the locations list
    result = db.user_trial.update_one(
        {'username': username},
        {'$addToSet': {'subscribed_locations': location}}  # $addToSet adds the item if it doesn't already exist
    )
    if result.modified_count:
        return Response({'status': 'Location added successfully'}, status=200)
    else:
        return Response({'error': 'User not found or location already exists'}, status=404)

@api_view(['POST']) 
def add_count_to_location(request):
    username = request.data.get('username')
    location = request.data.get('location')
    user = db.user_trial.find_one({'username': username})

    if location in user.get('subscribed_locations', []):
        subscription_cluster = db.subscription_trial.find_one({'location': location})
        if subscription_cluster is None:
            longitude, latitude = geocode_location(location)
            new_location = {
                'location': location,
                'subscribers': 1,
                'latitude': latitude,
                'longitude': longitude
            }
            result = db.subscription_trial.insert_one(new_location)

            # Check if the document was successfully inserted
            if result.inserted_id:
                return Response({'status': 'Added location to database'}, status=200)
            else:
                return Response({'status': 'Not able to add new location to sub database'}, status=404)

        else:
            document_id = subscription_cluster['_id']
            result = db.subscription_trial.update_one(
                {'_id': document_id},
                {'$inc': {'subscribers': 1}}
            )
            if result.modified_count:
                return Response({'status': 'Added subscription count for location'}, status=200)
            else:
                return Response({'status': 'Document not found or no update was needed'}, status=404)
    else:
        return Response({'error': 'User is not subscribed to location'}, status=404)
    
@api_view(['POST']) 
def remove_location(request):
    username = request.data.get('username')
    location = request.data.get('location')
    user = db.user_trial.find_one({'username': username})
    if not username or not location:
        return Response({'error': 'Username and location are required'}, status=400)
    if location not in user.get('subscribed_locations', []):
        return Response({'error': 'Location does not already exists for this user'}, status=400)
    
    # Remove the location from the user's 'locations' array
    result = db.user_trial.update_one(
        {'username': username},
        {'$pull': {'subscribed_locations': location}}
    )
    if result.modified_count:
        return Response({'status': 'Location removed successfully'}, status=200)
    else:
        return Response({'error': 'User not found or location not in list'}, status=404)

@api_view(['POST']) 
def remove_count_from_location(request):
    username = request.data.get('username')
    location = request.data.get('location')
    # user = db.user_trial.find_one({'username': username})
    # if location in user.get('subscribed_locations', []):
    subscription_cluster = db.subscription_trial.find_one({'location': location})
    if subscription_cluster == None:
        return Response({'error': 'Location not in subscription database'})
    count = subscription_cluster['subscribers']
    if count == 1:
        result = db.subscription_trial.delete_one({'location': location})
        if result.deleted_count:
            return Response({'status': 'Subscription deleted successfully'})
        else:
            return Response({'error': 'Subscription not found'}, status=404)
    elif count > 1:
        document_id = subscription_cluster['_id']
        result = db.subscription_trial.update_one(
            {'_id': document_id},
            {'$inc': {'subscribers': -1}}
        )
        if result.modified_count:
            return Response({'status': 'Removed subscription count for location'}, status=200)
        else: 
            return Response({'error': 'Could not remove location'}, status=400)
    return Response({'error': 'Could not fin dlocation in subscription database'}, status=400)
    # else:
    #     return Response({'error': 'User is not subscribed to location'}, status=404)















        
