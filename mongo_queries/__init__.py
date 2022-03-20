import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


password = os.getenv("PASSWORD")
mongo_user = os.getenv("MONGO_USER")
mongo_uri = f"mongodb+srv://{mongo_user}:{password}@cluster0.iep8o.azure.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
