import pymongo

atlas_url = 'mongodb+srv://598284:NayC8yGabCb6petB@subscription-db.nuxok2i.mongodb.net/'
atlas_client = pymongo.MongoClient(atlas_url)
atlas_db = atlas_client['FrontController']