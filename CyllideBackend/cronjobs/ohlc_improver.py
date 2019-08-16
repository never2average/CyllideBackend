import requests
import json
from datetime import datetime
from time import sleep
ohlc = {}

companyIDs = {
    "TCS": 8345,
    "INFY": 10960,
    "RELIANCE": 13215,
    "ONGC": 11599,
    "ZEEL": 11769,
    "TATAMOTORS": 12934,
    "YESBANK": 16552,
    "INDUSINDBK": 9196,
    "VEDL": 13111,
    "JSWSTEEL": 8352,
    "UPL": 6114,
    "HCLTECH": 4291,
    "TATASTEEL": 12902,
    "ICICIBANK": 9194,
    "IOC": 11924,
    "HEROMOTOCO": 13636,
    "GRASIM": 13696,
    "CIPLA": 13917,
    "BAJFINANCE": 11260,
    "SBIN": 11984,
    "HINDALCO": 13637,
    "TITAN": 12903,
    "INFRATEL": 22411,
    "HDFCBANK": 9195,
    "KOTAKBANK": 12161,
    "NTPC": 12316,
    "ASIANPAINT": 14034,
    "WIPRO": 12799,
    "ITC": 13554,
    "ADANIPORTS": 20316,
    "MARUTI": 11890,
    "AXISBANK": 9175,
    "EICHERMOT": 13787,
    "BHARTIARTL": 2718,
    "BAJAJ-AUTO": 21430,
    "HDFC": 13640,
    "COALINDIA": 11822,
    "ULTRACEMCO": 3027,
    "POWERGRID": 4628,
    "GAIL": 4845,
    "BAJAJFINSV": 21426,
    "BRITANNIA": 13934,
    "LT": 13447,
    "BPCL": 11941,
    "HINDUNILVR": 13616,
    "TECHM": 11221,
    "DRREDDY": 13841,
    "M&M": 11898,
    "SUNPHARMA": 9134,
    "IBULHSGFIN": 15580
}
home = "/home/ubuntu/data"
timestamp = datetime.now().strftime("%s")
timestamp = int(timestamp) * 1000
s = "https://json.bselivefeeds.indiatimes.com/ET_Community/companypagedata?companyid={}&_={}"
for i in companyIDs:
    r = requests.get(s.format(companyIDs[i], timestamp)).json()
    ohlc[i] = r["bseNseJson"][1]["lastTradedPrice"]
    sleep(1)
json.dump(
    ohlc,
    open(home + "/ohlc_nifty.json", "w+")
)
