import requests, os, tweepy
from helpers.tweepyClient import getTweepyClient
from helpers.top100coins import get_top_100_cryptos
import pymongo
from dotenv import load_dotenv

load_dotenv()

class TweetPrinterV2(tweepy.StreamingClient):

  top_100_coins_dict = get_top_100_cryptos()
  CHAT_ID = os.getenv("CHAT_TEST_ID")
  tweepyClient = getTweepyClient()
  TOKEN = os.getenv("TELEGRAM_GHOUL_TOKEN")
  
  def on_tweet(self, tweet):
  
    tickers = self.getTickers(tweet.text)
    
    url = f"https://twitter.com/{tweet.author_id}/status/{tweet.id}"

    if tickers:
      userObject = self.tweepyClient.get_user(id=tweet.author_id)

      username = userObject[0]["username"]
      fullName = userObject[0]["name"]

      tickerString = ""
      for ticker in tickers:
        tickerString += "$" + ticker + " "

      MESSAGE = f"{fullName} (@{username}) has tweeted {tickerString}\n\n{url}"

      self.postUrlToTelegram(MESSAGE)
      # self.check_keywords(tweet.text, ticker, url, userObject)
    else:
      print("no ticker:", tweet.text, " ", url)


  def postUrlToTelegram(self, MESSAGE):
    
    print("sending tweet to tg: ", MESSAGE)
    call = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={MESSAGE}"
    requests.get(call).json()


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


  def isInTop100(self, threeLetteres):
    try:
      get = self.top_100_coins_dict[threeLetteres.upper()]
    except KeyError:
      return False
    return True


  def checkForEachNarrative(self, tickers, text, narratives): 
    for narrative in narratives:
        # keywords =  query for keywords for each narrative
        keywords = []
        for narrative in narratives:
          self.checkForSingleNarrative(text, keywords)

  def checkForSingleNarrative(text, tickers, narrativeKeywords):

    text = text.lower()

    for keyword in narrativeKeywords:
        if keyword.lower() in text:
           pass
           # write to narrative table the ticker

def on_connect(self):
  
  print("connected")




