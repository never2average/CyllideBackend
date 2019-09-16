from models import Positions, Customers
import json
from keys import secret_key
import jwt
from statuscodes import unAuthorized, working
from datetime import datetime, timedelta
home = "/home/ubuntu/data/"


def listPositions(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = json.loads(
            Customers.objects.get(userName=tokenValidator[0]).to_json()
        )
        return json.dumps({"data": data["positionList"]}), working


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


def takePosition(token, ticker, quantity):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        cust = Customers.objects.get(userName=tokenValidator[0])
        fp = open(home+"ohlc_nifty.json")
        posList = Positions(
            ticker=ticker,
            quantity=int(quantity),
            entryPrice=json.load(fp)[ticker]
        )
        dobj = datetime.now() + timedelta(minutes=330)
        dobj = dobj.hour*60 + dobj.minute
        if len(cust.positionList) < 23 and dobj >= 0 and dobj < 930:
            if cust.positionList != []:
                cust.update(add_to_set__positionList=[posList])
            else:
                cust.update(
                    set__positionList=[posList],
                    inc__cyllidePoints=20
                )
            return json.dumps({"data": "Position Taken"}), working
        else:
            return json.dumps({"data": "Position Not Taken"}), working


def getLeaderBoard(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = Customers.objects.only(
            "userName", "cyllidePoints", "profilePic"
        ).order_by("-cyllidePoints").to_json()
        return json.dumps({"data": json.loads(data)}), working


def validateToken(token):
    try:
        username = jwt.decode(token, secret_key)["user"]
        try:
            cust = Customers.objects.get(userName=username)
            cust.update(set__lastLogin=datetime.today())
            return cust.userName, True
        except Exception:
            return None, False
    except Exception:
        return None, False
