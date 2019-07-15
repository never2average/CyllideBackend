from models import Positions, Customers
import json
from keys import secret_key
import jwt
from statuscodes import unAuthorized, working


def listPositions(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = json.loads(
            Customers.objects.get(userName=tokenValidator[0])
        )
        return json.dumps({"data": data["positionsList"]}), working


def takePosition(token, ticker, quantity):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = Customers.objects.get(userName=tokenValidator[0])
        pos = Positions(
            ticker=ticker,
            quantity=int(quantity)
        )
        data.update(add_to_set__positionsList=[pos])
        return json.dumps({"data": "Position Taken"}), working


def getLeaderBoard(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = Customers.objects.only(
            "userName", "numStreaks", "numDaysCurrentStreak"
        ).order_by("numStreaks", "numDaysCurrentStreak")
        data = json.loads(data.to_json())
        return json.dumps({"data": data}), working


def validateToken(token):
    try:
        username = jwt.decode(token, secret_key)["user"]
        try:
            cust = Customers.objects.get(userName=username)
            return cust.userName, True
        except Exception:
            return None, False
    except Exception:
        return None, False
