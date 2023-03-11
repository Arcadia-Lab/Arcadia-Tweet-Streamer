import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class dbOperator:

    mongoClient = MongoClient(f'''mongodb+srv://{os.getenv("MONGO_USERNAME")}:{os.getenv("MONGO_PASSWORD")}@cluster0.dvw7rbw.mongodb.net''')
    db = mongoClient["test"]

    def __init__(self) -> None:
        pass
    
    # Fill tweet document
    def storeTweetToDb(self, tickers, url, accountId, narratives):
        tweetsCollection = self.db["tweets"]
        
        # Do a query for twitter account that posted this here

        newTweet = {
            "tickers": tickers,
            "twitterUrl": url,
            "date": datetime.now(),
            "twitterAccount": "addhere", # here needed
            "narrative": narratives
        }

    # Fill twitter account document
    def fillTwitterAccountCollection(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(script_dir)
        file_path = os.path.join(script_dir + "\\textfile.txt")
        with open(file_path, "r") as f:
            lines = f.readlines()
            toTrackIdList = []
            for line in lines:
                line = line.strip()
                try:
                    toTrackIdList.append(line.split(" ")[1])
                except IndexError:
                    print(line)

            return toTrackIdList
            

    # Fill narrative document
    def fillNarrativeCollection(self):
        pass


operarorDb = dbOperator()

list = operarorDb.fillTwitterAccountCollection()

print(list)