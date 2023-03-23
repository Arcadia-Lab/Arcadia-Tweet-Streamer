import os

from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class dbOperator:

    mongoClient = MongoClient(f'''mongodb+srv://{os.getenv("MONGO_USERNAME")}:{os.getenv("MONGO_PASSWORD")}@cluster0.dvw7rbw.mongodb.net''')
    db = mongoClient["test"]


    def __init__(self) -> None:
        self.tweetsCollection = self.db["tweets"]
        self.twitterAccountCollection = self.db["twitteraccounts"]
        self.narrativeCollection = self.db["narratives"]


    def storeTweetToDb(self, tickers, url, twitterAcc, narrativeIds):
        
        twitterAccMongoId = twitterAcc["_id"]
        now = datetime.now()

        formattedDate = now.strftime('%Y-%m-%d %H:%M:%S')

        newTweetDoc = {
            "tickers": tickers,
            "twitterUrl": url,
            "date": formattedDate,
            "twitterAccount": twitterAccMongoId,
            "narrative": narrativeIds
        }

        self.tweetsCollection.insert_one(newTweetDoc)


    def getTwitterAccountByid(self, twitterId):
        return self.twitterAccountCollection.find_one({ "twitterId": twitterId })


    def getNarratives(self):
        narrativeObjects = list(self.narrativeCollection.find({}))
        return narrativeObjects


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

        for id in toTrackIdList:
            userObject = self.tweepyClient.get_user(id=id)
            username = userObject[0]["username"]
            fullName = userObject[0]["name"]
            
            url = f"https://twitter.com/{username}"
            accountDoc = {
                "fullName": fullName,
                "username": username,
                "twitterId": id,
                "twitterUrl": url
            }

            self.twitterAccountCollection.insert_one(accountDoc)


    def fillNarrativeCollection(self):
            narrativeName = [
                "ZK", "Arbitrum", "Optimism", "AI", "NftFi", "Metaverse", "China", "Perps", "BSC", "Solidly"
            ]

            keywords = [" binance ", " bsc ", " bnb "]
            self.narrativeCollection.update_one({ "name": "BSC" }, { "$set": { "keywords": keywords } })


    def getUndefinedNarrativeId(self):
        undefined_narrative = self.narrativeCollection.find_one({"name": "Undefined"})
        return undefined_narrative.get('_id')
    

    def deleteAllTweets(self):
        result = self.tweetsCollection.delete_many({})
        print(f"Deleted {result.deleted_count} documents")


    def addEmptyArrToUndefinedNarr(self):
        result = self.narrativeCollection.update_one({"name": "Undefined"}, {"$set": {"keywords": []}})

