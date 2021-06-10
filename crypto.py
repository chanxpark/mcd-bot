from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os


def get_crypto(symbol):
    API_KEY = os.environ["CRYPTO_API_KEY"]

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {"symbol": symbol, "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        if response.ok:
            data = json.loads(response.text)
            return data["data"][symbol]
        else:
            return "error"
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return "error"
