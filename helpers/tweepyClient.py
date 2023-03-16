import tweepy
from dotenv import load_dotenv
import os

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN_3")

def getTweepyClient():
    return tweepy.Client(bearer_token)
