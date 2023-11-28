from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from bson.errors import InvalidId

from .serializers import LocationSerializer
from db_connection import db

@api_view(['GET'])
def get_locations(request):
    locations = list(db.subscription_trial.find())
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_location(request):
    location_data = request.data.get('location')
    existing_location = db.subscription_trial.find_one({'location': location_data})

    if existing_location:
        return Response({'error': 'Location already exists'}, status=409)
    
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)

# @api_view(['PUT'])
# def update_location(request, location_id):
#     try:
#         obj_id = ObjectId(location_id)
#     except InvalidId:
#         return Response({'error': 'Invalid location ID format'}, status=400)

#     # Update a specific location
#     location = db.subscription_trial.find_one({'_id': obj_id})
#     if not location:
#         return Response({'error': 'Location not found'}, status=404)

#     serializer = LocationSerializer(location, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=200)
#     return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_location(request):
    location_data = request.data.get('location')
    existing_location = db.subscription_trial.find_one({'location': location_data})

    if existing_location:
        delete_result = db.subscription_trial.delete_one({'_id': existing_location['_id']})
        if delete_result.deleted_count > 0:
            return Response({'status': 'Deleted location from subscription database'}, status=204)
        else:
            return Response({'error': 'No location was deleted'}, status=404)
    else:
        return Response({'error': 'Location not found in subscription database'}, status=404)
