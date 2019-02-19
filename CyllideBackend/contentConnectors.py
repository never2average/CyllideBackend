from models import Customers, Content
from keys import secret_key, data_encryption_key
from statuscodes import unAuthorized, working
from datetime import datetime
from simplecrypt import encrypt, decrypt
import json
import jwt


def viewStories(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[0]:
        return encrypt(
            data_encryption_key,
            json.dumps(
                {"data": "Need to login first"}
                ).encode('utf-8')
            ), unAuthorized
    else:
        contentData = json.loads(Content.objects.get().to_json())
        return encrypt(
            data_encryption_key, json.dumps(
                {"data": contentData}
                ).encode('utf-8')
            ), working


def validateToken(token):
    try:
        username = jwt.decode(token, secret_key)["user"]
        try:
            cust = Customers.objects.get(userName=username)
            return cust.userName, True
        except:
            return None, False
    except:
        return None, False
