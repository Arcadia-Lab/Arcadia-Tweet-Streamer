import json
import requests, os, tweepy
from dotenv import load_dotenv

from helpers.tweepyClient import getTweepyClient
from helpers.top100coins import get_top_100_cryptos

from classes.dbOperator import dbOperator

load_dotenv()

class TweetPrinterV2(tweepy.StreamingClient):

  TELEGRAM_CHAT_ID = os.getenv("CHAT_PRODUCTION_ID")
  TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_GHOUL_TOKEN")
  tweepyClient = getTweepyClient()
  dbOperator = dbOperator()
  top_100_coins_dict = get_top_100_cryptos()


  def on_tweet(self, tweet):
    
    tickers = self.getTickers(tweet.text)
    
    url = f"https://twitter.com/{tweet.author_id}/status/{tweet.id}"

    if tickers:
      tickerString = self.createTickerString(tickers)

      twitterAcc = self.dbOperator.getTwitterAccountByid(str(tweet.author_id))

      MESSAGE = self.createTgMessage(url, tickerString, twitterAcc)

      self.postUrlToTelegram(MESSAGE)

      self.postToDiscord(MESSAGE)

      narrativeIds = self.extractNarratives(tweet.text)

      self.dbOperator.storeTweetToDb(tickers, url, twitterAcc, narrativeIds)

    else:
      print(f"NO tickers in the following tweet:\n{tweet.text}\nthat is with the following url: {url}\n")


  def getTickers(self, text):
    tickers = []
    for word in text.split(" "):
        if word.startswith("$") and not word[1:].isdigit():
            ticker = word[1:].upper()
            if len(ticker) == 3 or len(ticker) == 4:
                threeLetters = ticker[:3]
                if not self.isInTop100(threeLetters):
                    tickers.append(ticker)
    return tickers
  

  def createTickerString(self, tickers):
      tickerString = ""
      for ticker in tickers:
        tickerString += "$" + ticker + " "

      return tickerString
  

  def createTgMessage(self, url, tickerString, twitterAcc):
     return f"""{twitterAcc["fullName"]} (@{twitterAcc["username"]}) has tweeted {tickerString}\n\n{url}"""


  def postUrlToTelegram(self, MESSAGE):
    call = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={self.TELEGRAM_CHAT_ID}&text={MESSAGE}"
    requests.get(call).json()
    print(f"tweet sent to tg with the message of: {MESSAGE}")


  def postToDiscord(self, MESSAGE):
     url = "https://discord.com/api/webhooks/1088414836301496411/HxjPldbOEAzSgLprFehTvTy_v5BKuG7rSUsAviFaZrDKz2icjhksgCMxPJ1lHhzJNVDz"
     data = {"content": MESSAGE}
     payload = json.dumps(data)
     requests.post(url, data=payload, headers={"Content-Type": "application/json"})


  def extractNarratives(self, text):
    narrative_objects = self.dbOperator.getNarratives()
    narrative_keywords = [narrative.get("keywords", []) for narrative in narrative_objects]
    
    text = text.lower()

    extracted_narrative_ids = []
    for i, keywords in enumerate(narrative_keywords):
        for keyword in keywords:
            if keyword.lower() in text:
                extracted_narrative_ids.append(narrative_objects[i]["_id"])

    try:
       extracted_narrative_ids[0]
    except:
       extracted_narrative_ids.append(self.dbOperator.getUndefinedNarrativeId())
        

    return extracted_narrative_ids


  def isInTop100(self, threeLetteres):
    try:
      get = self.top_100_coins_dict[threeLetteres.upper()]
    except KeyError:
      return False
    return True


  def on_connect(self):
    print("connected to tweet streamer")




