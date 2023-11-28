from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from db_connection import db

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=128)
    subscribed_locations = serializers.ListField(child=serializers.CharField(max_length=100))

    def validate_username(self, value):
        if db.user_trial.count_documents({'username': value}) > 0:
            raise serializers.ValidationError("A user with that username already exists.")
        return value
    
    def create(self, validated_data):
        # Handle user creation with Pymongo
        # validated_data['password'] = make_password(validated_data['password'])
        validated_data['password'] = make_password(validated_data['password'])
        db.user_trial.insert_one(validated_data)
        return validated_data

    def update(self, instance, validated_data):
        # Handle updating user data
        if 'password' in validated_data:
            # Check if the new password is already hashed, hash if not
            if not check_password(validated_data['password'], instance.get('password')):
                validated_data['password'] = make_password(validated_data['password'])

        db.user_trial.update_one({'username': instance['username']}, {'$set': validated_data})
        return validated_data


    
    

