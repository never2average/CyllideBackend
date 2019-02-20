from models import Customers, Content
from keys import secret_key, data_encryption_key
from statuscodes import unAuthorized, working
from datetime import datetime
from simplecrypt import encrypt, decrypt
import json
import jwt


def viewStories(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[0]:
        return encrypt(
            data_encryption_key,
            json.dumps(
                {"data": "Need to login first"}
                ).encode('utf-8')
            ), unAuthorized
    else:
        data = json.loads(decrypt(data_encryption_key, data).decode('utf-8'))
        contentData = json.loads(
            Content.objects.get(contentType=data["type"]).to_json()
            )
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
        except Exception:
            return None, False
    except Exception:
        return None, False
