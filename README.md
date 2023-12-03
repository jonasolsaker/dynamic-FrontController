# dynamic-FrontController

## Setup 
Need to download docker and have that on your computer. <br /><br />
To run docker image locally, run the following command:<br />
```docker build -t dynamic-frontcontroller:latest .; docker stop dynamic-frontcontroller; docker rm dynamic-frontcontroller; docker run --name dynamic-frontcontroller -d -p 8000:8000 dynamic-frontcontroller:latest; docker ps```

## Local database
If you want to test with a local database, change setup in ```db_connection.py``` file to similar to this: <br/>
```
url = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(url)

db = client['User_db']
```

## VSCode endpoint testing
```.rest``` files have testing for endpoints defined. To run on VSCode ```REST Client``` extention is needed.
