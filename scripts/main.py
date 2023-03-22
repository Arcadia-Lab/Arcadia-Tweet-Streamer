import sys, os, time
import keep_alive
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classes.TweetStreamer import TweetStreamer

def streamTweets():

    BEARER_TOKEN = os.getenv("BEARER_TOKEN_1")

    streamerOne = TweetStreamer(BEARER_TOKEN)

    streamerOne.startStreaming()

streamTweets()

## Run this in production
# while True:

#   try:
#     streamTweets()
#   except:
#     print("something went wrong: retry in 15secs: ")
#     time.sleep(15)
#     continue