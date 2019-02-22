import random
from models import TempAcc, Customers
import requests
import jwt
from keys import secret_key
from datetime import datetime, timedelta
from statuscodes import working, invalidLoginCredentials, userCreated
import mongoengine
mongoengine.connect("FUCKALL")


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
    except:
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
