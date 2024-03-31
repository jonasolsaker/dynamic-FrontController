import pymongo

atlas_url = 'mongodb://localhost:27017/' #change to correct atlas address when running, since project now is public
atlas_client = pymongo.MongoClient(atlas_url)
atlas_db = atlas_client['FrontController']

frontcontroller_db = atlas_client['FrontController_prod']