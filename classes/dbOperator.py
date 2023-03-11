from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class dbOperator:

    mongoClient = MongoClient(f'''mongodb+srv://{os.getenv("MONGO_USERNAME")}:{os.getenv("MONGO_PASSWORD")}@cluster0.dvw7rbw.mongodb.net''')
    db = mongoClient["test"]

    def __init__(self) -> None:
        pass

    def test(self):
        collection_names = self.db.list_collection_names()
        print(collection_names)



operarorDb = dbOperator()

operarorDb.test()