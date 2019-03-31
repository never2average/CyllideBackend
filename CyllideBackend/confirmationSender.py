import random
from models import TempAcc, Customers
import requests
import jwt
from keys import secret_key
from datetime import datetime, timedelta
from statuscodes import working, invalidLoginCredentials, userCreated
import mongoengine
import json


def generate_code():
    return str(random.randrange(100000, 999999))


def sendOTP(phone_num, username):
    try:
        otp = generate_code()
        message = """Thanks, for registering on cyllide,
        your One-Time Password is : {}""".format(otp)
        auth_key = "264217ATk5GD4QyM5c6f1772"
        req = requests.get(
            "http://api.msg91.com/api/sendhttp.php?country=91" +
            "&sender=CYLLID" +
            "&route=4" +
            "&mobiles=" + str(phone_num) +
            "&authkey=" + auth_key +
            "&message=" + message
            )
        print(req.status_code)
        tempAcc = TempAcc(
            toNumber=phone_num,
            otp=otp,
            username=username
        )
        tempAcc.save()
        return {"message": "MessageSendingSuccessful"}, working
    except Exception:
        return {"message": "MessageSendingFailed"}, 510


def verifyOTP(phone_num, otp, referee=None):
    try:
        tempAcc = TempAcc.objects.get(toNumber=phone_num, otp=otp)
        try:
            cust = Customers(
                userName=tempAcc.username,
                phoneNumber=phone_num
            )
            cust.save()
            token = jwt.encode({
                "user": cust.userName,
                "exp": datetime.utcnow() + timedelta(days=365)
                }, secret_key)
            if referee is not None:
                rewardReferrals(cust.userName, referee)
            return {"token": token.decode('UTF-8')}, userCreated

        except mongoengine.errors.NotUniqueError:
            cust = Customers.objects.get(userName=tempAcc.username)
            token = jwt.encode({
                "user": cust.userName,
                "exp": datetime.utcnow() + timedelta(days=365)
                }, secret_key)
            return {"token": token.decode('UTF-8')}, working
    except Exception:
        return {"message": "InvalidOTPEntered"}, invalidLoginCredentials


def rewardReferrals(userName, referee):
    cust = Customers.objects.get(userName=userName)
    cust.update(set__referralJoinedFrom=referee)
    cust.update(set__numCoins=cust.numCoins+3)
    cust = Customers.objects.get(userName=referee[:-4])
    cust.update(set__numberReferrals=cust.numberReferrals+1)
    cust.update(set__numCoins=cust.numCoins+3)


def getPicURL(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"data": "Login First"}, invalidLoginCredentials
    else:
        return {"data": json.loads(Customers.objects(userName=tokenValidator[0]).only("profilePic").to_json())}, working


def setPicURL(token, profileURL):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"data": "Login First"}, invalidLoginCredentials
    else:
        try:
            cust = Customers.objects.get(userName=tokenValidator[0])
            cust.update(set__profilePic=profileURL)
            return json.loads({"data": "ProfilePicUpdated"}), working
        except Exception:
            return {"data": "ProfilePicUpdateFailed"}, working


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
