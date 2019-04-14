import random
from models import TempAcc, Customers, Portfolios, Questions
import requests
import jwt
from keys import secret_key
from datetime import datetime, timedelta
from statuscodes import working, invalidLoginCredentials, userCreated
import mongoengine
import json
import smtplib, ssl


def generateCode():
    return str(random.randrange(100000, 999999))


def sendOTP(phone_num, username):
    try:
        try:
            cust = Customers.objects.get(phoneNumber=phone_num,userName=username)
        except Exception:
            try:
                cust = Customers.objects.get(phoneNumber=phone_num)
                return {"message": "InvalidUsername"}, working
            except Exception:
                pass
        otp = generateCode()
        message = """Thanks, for registering on Cyllide, your One-Time Password is : {}""".format(otp)
        auth_key = "264217ATk5GD4QyM5c6f1772"
        req = requests.get(
            "http://api.msg91.com/api/sendhttp.php?country=91" +
            "&sender=CYLLID" +
            "&route=4" +
            "&mobiles=" + str(phone_num) +
            "&authkey=" + auth_key +
            "&message=" + message
            )
        tempAcc = TempAcc(
            toNumber=phone_num,
            otp=otp,
            username=username
        )
        tempAcc.save()
        resp = {"message": "MessageSendingSuccessful"}
        try:
            cust = Customers.objects.get(phoneNumber=phone_num, userName=username)
            resp["firstTimeUser"] = False
        except Exception:
            resp["firstTimeUser"] = True
        return resp, working
    except Exception:
        return {"message": "MessageSendingFailed"}, working


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
            return {"token": token.decode('UTF-8'), "coins": cust.numCoins, "referralCode": cust.referralCode}, userCreated

        except mongoengine.errors.NotUniqueError:
            cust = Customers.objects.get(userName=tempAcc.username)
            token = jwt.encode({
                "user": cust.userName,
                "exp": datetime.utcnow() + timedelta(days=365)
                }, secret_key)
            return {"token": token.decode('UTF-8'), "coins": cust.numCoins, "referralCode": cust.referralCode}, working
    except Exception:
        return {"message": "InvalidOTPEntered"}, working


def rewardReferrals(userName, referee):
    cust = Customers.objects.get(userName=userName)
    cust.update(set__referralJoinedFrom=referee)
    cust.update(set__numCoins=cust.numCoins+1)
    cust = Customers.objects.get(userName=referee[:-4])
    cust.update(set__numberReferrals=cust.numberReferrals+1)
    cust.update(set__numCoins=cust.numCoins+3)


def getPicURL(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Login First"}), invalidLoginCredentials
    else:
        return json.dumps({"data": json.loads(Customers.objects(userName=tokenValidator[0]).only("profilePic").to_json())}), working


def setPicURL(token, profileURL):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"data": "Login First"}, invalidLoginCredentials
    else:
        try:
            cust = Customers.objects.get(userName=tokenValidator[0])
            cust.update(set__profilePic=profileURL)
            Portfolios.objects(portfolioOwner=cust.e)
            return json.dumps({"data": "ProfilePicUpdated", "url": profileURL}), working
        except Exception:
            return json.dumps({"data": "ProfilePicUpdateFailed"}), working


def getProfileInfo(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Login First"}), invalidLoginCredentials
    else:
        cust = json.loads(Customers.objects.get(userName=tokenValidator[0]).to_json())
        stats = {}
        stats["contestsParticipated"] = len(cust["contestsActiveID"])
        stats["contestsWon"] = cust["contestsWon"]
        stats["quizzesWon"] = cust["quizzesWon"]
        stats["quizzesParticipated"] = cust["quizzesParticipated"]
        stats["questionsAsked"] = cust["questionsAsked"]
        stats["questionsAnswered"] = cust["questionsAnswered"]
        stats["numUpvotes"] = cust["numUpvotes"]
        stats["numberReferrals"] = cust["numberReferrals"]
        stats["userName"] = cust["userName"]
        stats["numCoins"] = cust["numCoins"]
        return json.dumps({"data": stats}), working


def getProfileInfoOthers(token, username):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Login First"}), invalidLoginCredentials
    else:
        cust = json.loads(Customers.objects.get(userName=username).to_json())
        stats = {}
        stats["contestsParticipated"] = len(cust["contestsActiveID"])
        stats["contestsWon"] = cust["contestsWon"]
        stats["quizzesWon"] = cust["quizzesWon"]
        stats["quizzesParticipated"] = cust["quizzesParticipated"]
        stats["questionsAsked"] = cust["questionsAsked"]
        stats["questionsAnswered"] = cust["questionsAnswered"]
        stats["numUpvotes"] = cust["numUpvotes"]
        stats["numberReferrals"] = cust["numberReferrals"]
        stats["userName"] = cust["userName"]
        stats["numCoins"] = cust["numCoins"]
        stats["profilePic"] = cust["profilePic"]
        return json.dumps({"data": stats}), working


def sendFeedback(token, text):
    try:
        port = 465
        smtp_server = "smtp.gmail.com"
        sender_email = "batchjobrocks@gmail.com"
        receiver_email = "prasannkumar1263@gmail.com"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, "Password##123")
            server.sendmail(sender_email, receiver_email, text)
        return json.dumps({"data": "Email sent successfully"}), 200
    except Exception:
        return json.dumps({"data": "Email sending failed"}), 401


def checkUsernameValidity(phone_num, user_name):
    try:
        cust = Customers.objects.get(phoneNumber=phone_num)
        return json.dumps({"status": "available"}), working
    except Exception:
        try:
            cust = Customers.objects.get(userName=user_name)
            return json.dumps({"status": "taken"}), working
        except Exception:
            return json.dumps({"status": "available"}), working


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
