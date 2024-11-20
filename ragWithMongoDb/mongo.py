import pymongo
#from google.colab import userdata


from env import mongoURl

def get_mongo_client():
  mongo_uri = mongoURl
  """Establish connection to the MongoDB."""
  try:
    client = pymongo.MongoClient(mongo_uri)
    print("Connection to MongoDB successful")
    return client
  except pymongo.errors.ConnectionFailure as e:
    print(f"Connection failed: {e}")
    return None

mongo_client = get_mongo_client()