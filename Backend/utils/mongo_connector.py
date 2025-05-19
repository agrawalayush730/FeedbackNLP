from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["feedback_analyzer"]
feedback_collection = db["analyzed_feedback"]

def save_feedback_to_mongo(data: dict):
    feedback_collection.insert_one(data.copy())
