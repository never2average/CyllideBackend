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


def takePosition(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        cust = Customers.objects.get(userName=tokenValidator[0])
        posList = []
        data = json.loads(data)
        for i in data:
            posList.append(
                Positions(
                    ticker=i["ticker"],
                    quantity=int(i["quantity"])
                )
            )
        cust.update(add_to_set__positionsList=[posList])
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
            cust.update(set__lastLogin=datetime.today())
            return cust.userName, True
        except Exception:
            return None, False
    except Exception:
        return None, False
