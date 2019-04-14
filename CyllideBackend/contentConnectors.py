from models import Customers, Content
from keys import secret_key, data_encryption_key
from statuscodes import unAuthorized, working
import json
import jwt


def viewStories(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        contentData = json.loads(
            Content.objects().exclude("contentHits","readingTime").limit(10).to_json())
        return json.dumps({"data": contentData}), working


def updateStories(token, contentID, timeInMins):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        cont = Content.objects.get(id=contentID)
        cont.update(set__contentHits=cont.contentHits+1)
        cont.update(add_to_set__readingTime=[timeInMins])
        return json.dumps({"data":"data addition successful"})


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
