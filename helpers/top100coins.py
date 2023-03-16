import requests

def get_top_100_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": "100",
        "page": "1",
        "sparkline": "false",
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    cryptos = {}
    for crypto in response.json():
        cryptos[crypto["symbol"].upper()] = None
    return cryptos



