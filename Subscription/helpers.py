def geocode_location(location):
    # Call to an external geocoding service
    # Replace this with actual call to a geocoding API
    # For example, you might use requests.get() to call an API
    # Here, we are just returning dummy coordinates
    locationList = location.split(",")
    longitude = locationList[0]
    latitude = locationList[1]
    return (longitude, latitude)
