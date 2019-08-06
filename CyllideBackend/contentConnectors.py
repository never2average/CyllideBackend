from models import Customers, Content, Shorts
from keys import secret_key
from datetime import datetime
from statuscodes import unAuthorized, working
import json
import jwt


def viewStories(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        contentData = json.loads(
            Content.objects().exclude(
                "contentHits", "readingTime"
            ).limit(10).to_json()
        )
        return json.dumps({"data": contentData}), working


def updateStories(token, contentID, timeInMins):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        cont = Content.objects.get(id=contentID)
        cont.update(set__contentHits=cont.contentHits+1)
        cont.update(add_to_set__readingTime=[timeInMins])
        return json.dumps({"data": "data addition successful"}), working


def inshortsViewer(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = Shorts.objects.order_by("forday-").limit(10).to_json()
        return json.dumps({"data": json.loads(data)}), working


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
