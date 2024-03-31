from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
from db_connection import atlas_db, frontcontroller_db    
    
def requestFireRisk(location):
    frs_firerisk_url = 'http://localhost:8000/frs/firerisk/ttf/'
    try:
        frs_response = requests.get(frs_firerisk_url, params={'location': location})
        frs_data = frs_response.json()
        return frs_data
    except Exception as e:
        return JsonResponse({'error': 'Failed to retrieve ttf from FRS', 'details': str(e)}, status=500)

def requestFireRiskFactor(location):
    frs_firerisk_url = 'http://localhost:8000/frs/firerisk/factor/'
    try:
        frs_response = requests.get(frs_firerisk_url, params={'location': location})
        frs_data = frs_response.json()
        return frs_data
    except Exception as e:
        return JsonResponse({'error': 'Failed to retrieve fire risk factor from FRS', 'details': str(e)}, status=500)
    
def addCountLocation(location):
    location_document = frontcontroller_db.Subscription.find_one({'location': location})
    if location_document is not None:
        new_subscriber_count = location_document['subscriberCount'] + 1
        frontcontroller_db.Subscriptions.update_one({'_id': location_document['_id']}, {'$set': {'subscriberCount': new_subscriber_count}})
        return True
    return False
    

@api_view(['GET'])
def fireRisk(request):
    if 'location' in request.query_params:
        location = request.query_params['location']
        try:
            longitude, latitude = [float(coord) for coord in location.split(',')]
        except ValueError:
            return JsonResponse({'error': 'Invalid location format'}, status=400)
    else:
        data = request.data
        location = data['location']
    subscription_document = frontcontroller_db.Subscription.find_one({'location': location})
    if subscription_document:
        pass
    else:
        pass
    
    fire_risk = requestFireRisk(location)
    return JsonResponse({'FireRisk': fire_risk})


@api_view(['GET'])
def fireRiskFactor(request):
    if 'location' in request.query_params:
        location = request.query_params['location']
        try:
            longitude, latitude = [float(coord) for coord in location.split(',')]
        except ValueError:
            return JsonResponse({'error': 'Invalid location format'}, status=400)
    else:
        data = request.data
        location = data['location']
        
    fire_risk_factor = requestFireRiskFactor(location)
    return JsonResponse({'FireRiskFactor': fire_risk_factor})



@api_view(['POST', 'DELETE', 'GET'])
def location(request):
    if 'location' in request.query_params:
        location = request.query_params['location']
        try:
            longitude, latitude = [float(coord) for coord in location.split(',')]
        except ValueError:
            return JsonResponse({'error': 'Invalid location format'}, status=400)
    else:
        data = request.data
        location = data['location']
    
    if request.method == 'POST':
        frontcontroller_db.Subscriptions.insert_one({'location': location, 'subscriberCount': 1})
        return JsonResponse({'Inserted location': f'Inserted location {location} into subscription database'}, status=200)
    elif request.method == 'DELETE':
        frontcontroller_db.Subscriptions.delete_one({'location': location})
        return JsonResponse({'Deleted location': f'Deleted location {location} from subscription database'}, status=200)
    elif request.method == 'GET':
        document = frontcontroller_db.Subscriptions.find_one({'location': location})
        return JsonResponse({'LocationData': document}, status=200)
    
    frontcontroller_db.Subscriptions.insert_one({'location': location, 'subscriberCount': 1})
    return JsonResponse({'Inserted location': f'Inserted location {location} into subscription database'}, status=200)



@api_view(['PATCH'])
def increaseSubscriberCount(request):
    if 'location' in request.query_params:
        location = request.query_params['location']
    else:
        data = request.data
        location = data['location']
    
    subscription_document = frontcontroller_db.Subscriptions.find_one({'location': location})
    if subscription_document is not None:
        subscription_document['subscriberCount'] = subscription_document.get('subscriberCount', 0) + 1
        frontcontroller_db.Subscriptions.replace_one({'_id': subscription_document['_id']}, subscription_document)
        return JsonResponse({'Increased count': f'Increased subscriber count for location: {location}'}, status=200)
    return JsonResponse({'error': 'Could not find wanted location in subscription database'}, status=400)


@api_view(['PATCH'])
def decreaseSubscriberCount(request):
    if 'location' in request.query_params:
        location = request.query_params['location']
    else:
        data = request.data
        location = data['location']
    
    subscription_document = frontcontroller_db.Subscriptions.find_one({'location': location})
    if subscription_document is not None:
        if subscription_document['subscriberCount'] == 0:
            frontcontroller_db.Subscriptions.delete_one({'_id': subscription_document['_id']})
            return JsonResponse({'Deleted document': 'No more subscribers, location is deleted'}, status=200)
        else:
            subscription_document['subscriberCount'] = subscription_document.get('subscriberCount', 0) - 1
            frontcontroller_db.Subscriptions.replace_one({'_id': subscription_document['_id']}, subscription_document)
            return JsonResponse({'Decreased count': f'Increased subscriber count for location: {location}'}, status=200)
    return JsonResponse({'error': 'Could not find wanted location in subscription database'}, status=400)