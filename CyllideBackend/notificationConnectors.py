from models import Notifications, Customers
import json
from keys import secret_key
import jwt
from statuscodes import unAuthorized, working
from mongoengine.queryset.visitor import Q
from datetime import datetime


def getMyNotifications(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        notificationList = Notifications.objects(
            username=tokenValidator[0],
            isRead=False
            )
        # print(notificationList.to_json())
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
            cust.update(set__lastLogin=datetime.today())
            return cust.userName, True
        except Exception:
            return None, False
    except Exception:
        return None, False


# if __name__ == "__main__":
#     notification = Notifications(
#         username="None",
#         message="First Test Notification",
#         notificationTime=datetime.now(),
#         isRead=False
#     )
#     notification.save()
#     print("Here")
#     notification = Notifications(
#         username="None",
#         message="First Test Notification",
#         notificationTime=datetime.now(),
#         isRead=True
#     )
#     notification.save()
#     print("Here")
#     getMyNotifications("edhjksnshvdwbkjnxm,")
