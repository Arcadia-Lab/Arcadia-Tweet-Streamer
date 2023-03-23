import sys, os, time
from keep_alive import keep_alive

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classes.TweetStreamer import TweetStreamer


def streamTweets():

  BEARER_TOKEN = os.getenv("BEARER_TOKEN_PRODUCTION")

  streamerOne = TweetStreamer(BEARER_TOKEN)

  streamerOne.startStreaming()


## Run this in production
while True:

  try:
    keep_alive()
    streamTweets()
  except:
    print("retry in 15secs: ")
    time.sleep(15)
    continue
