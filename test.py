from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
print(MONGO_PASSWORD)
print(MONGO_USERNAME)
MONGO_URL = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.dvw7rbw.mongodb.net"
# Connect to the MongoDB server
client = MongoClient(MONGO_URL)

# Get the database object
db = client["test"]

# Get the collection object
collection = db["twitteraccounts"]

# Create a document to insert into the collection
document = {"fullName": "John Doe", "username": "errrxd", "twitterId": "johndoe@edddxample.com"}

# Insert the document into the collection
result = collection.insert_one(document)

# Get the inserted document by its ID
inserted_doc = collection.find_one({"_id": result.inserted_id})

# Print the inserted document
print(inserted_doc)
