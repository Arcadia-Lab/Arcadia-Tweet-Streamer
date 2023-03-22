import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.top100coins import get_top_100_cryptos


top_100_coins_dict = get_top_100_cryptos()

def isInTop100(threeLetteres):
    try:
        get = top_100_coins_dict[threeLetteres.upper()]
    except KeyError:
        return False
    return True

def getTickers(text):
    tickers = []
    for word in text.split(" "):
        if word.startswith("$") and not word[1].isdigit():
            ticker = word[1:].upper()
            if len(ticker) == 3 or len(ticker) == 4:
                threeLetters = ticker[:3]
                if not isInTop100(threeLetters):
                    tickers.append(ticker)
    return tickers

# def getTickers(text):
#     tickers = []
#     for word in text.split(" "):
#         if word.startswith("$"):
#             # print(word)
#             tickers.append(word)
#     return tickers



text = '''Break & retest the resistance, then it's off for $OPTI 

 start up raise is currently at $42M+ with 15k + supporters. These numbers don't come so often, the demand is insanely strong.  (https://gate.io/startup/738)

Wouldn't be suprised to see it ranging around $1 in a day or two with the Gate Io listing, It's ON.'''

tickers = getTickers(text)

print(tickers)