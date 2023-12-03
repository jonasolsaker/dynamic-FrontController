from rest_framework import serializers
from db_connection import atlas_db
from .helpers import geocode_location

class LocationSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=17)
    latitude = serializers.CharField(max_length=8, read_only=True)
    longitude = serializers.CharField(max_length=8, read_only=True)
    subscribers = serializers.IntegerField(default=0)

    def validate_latitude(self, value):
        # Add validation logic for latitude
        return value

    def validate_longitude(self, value):
        # Add validation logic for longitude
        return value

    def create(self, validated_data):
        longitude, latitude = geocode_location(validated_data['location'])

        validated_data['latitude'] = latitude
        validated_data['longitude'] = longitude
        
        atlas_db.subscription_trial.insert_one(validated_data)
        return validated_data

    def update(self, instance, validated_data):
        atlas_db.subscription_trial.update_one({'_id': instance['_id']}, {'$set': validated_data})
        return validated_data

    def add_subscriber(self, location_id):
        atlas_db.subscription_trial.update_one({'_id': location_id}, {'$inc': {'subscribers': 1}})

    def remove_subscriber(self, location_id):
        atlas_db.subscription_trial.update_one({'_id': location_id}, {'$inc': {'subscribers': -1}})
