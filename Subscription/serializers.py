from rest_framework import serializers
from db_connection import db
from .helpers import geocode_location

class LocationSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=17)
    latitude = serializers.CharField(max_length=8, read_only=True)
    longitude = serializers.CharField(max_length=8, read_only=True)
    subscribers = serializers.IntegerField(default=0)

    def validate_latitude(self, value):
        # Add validation logic for latitude if needed
        return value

    def validate_longitude(self, value):
        # Add validation logic for longitude if needed
        return value

    def create(self, validated_data):
        # Geocode the location to get latitude and longitude
        longitude, latitude = geocode_location(validated_data['location'])

        validated_data['latitude'] = latitude
        validated_data['longitude'] = longitude
        
        # Insert the document into MongoDB
        db.subscription_trial.insert_one(validated_data)
        return validated_data

    def update(self, instance, validated_data):
        # Add logic to update an existing location document
        # Instance here would typically be a dictionary with the location's current data
        db.subscription_trial.update_one({'_id': instance['_id']}, {'$set': validated_data})
        return validated_data

    def add_subscriber(self, location_id):
        # Increment the subscriber count for a given location
        db.subscription_trial.update_one({'_id': location_id}, {'$inc': {'subscribers': 1}})

    def remove_subscriber(self, location_id):
        # Decrement the subscriber count for a given location
        db.subscription_trial.update_one({'_id': location_id}, {'$inc': {'subscribers': -1}})
