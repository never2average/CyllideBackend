from models import Notifications, Customers
import json
from keys import secret_key
import jwt
from statuscodes import unAuthorized, working


def getMyNotifications(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        notificationList = Notifications.objects(username=tokenValidator[0])
        return json.dumps(
            {"data": json.loads(notificationList.to_json())}
        ), working


def markAsRead(token, notificationID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        notification = Notifications.objects.get(id=notificationID)
        notification.update(set__isRead=True)
        return json.dumps(
            {"data": "Notification Read"}
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
