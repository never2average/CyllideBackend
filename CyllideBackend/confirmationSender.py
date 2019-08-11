import random
from models import TempAcc, Customers
import requests
import jwt
from keys import secret_key, msg91_authkey
from datetime import datetime, timedelta
from statuscodes import working, invalidLoginCredentials, userCreated
import mongoengine
import json
import ssl
import smtplib


def generateCode():
    return str(random.randrange(1000, 9999))


def sendOTP(phone_num):
    otp = generateCode()
    try:
        cust = Customers.objects.get(phoneNumber=phone_num)
    except Exception:
        pass
    else:
        message = "Your one-time password for cyllide is : {}.".format(otp)
        message += "Donot share this otp with anyone under any circumstances."
        req = requests.get(
            "http://api.msg91.com/api/sendhttp.php?country=91" +
            "&sender=CYLLID" +
            "&route=4" +
            "&mobiles=" + str(phone_num) +
            "&authkey=" + msg91_authkey +
            "&message=" + message
        )
        if req.status_code == 200:
            tempAcc = TempAcc(
                toNumber=phone_num,
                otp=otp
            )
            tempAcc.save()
            return {"message": "MessageSendingSuccessful"}, working
        else:
            return {"message": "MessageSendingFailed"}, working
    #     message = "Thanks for registering with Cyllide. "
    #     message = message + "Your one-time password is : {}.".format(otp)
    #     req = requests.get(
    #         "http://api.msg91.com/api/sendhttp.php?country=91" +
    #         "&sender=CYLLID" + "&route=4" + "&mobiles=" + str(phone_num) +
    #         "&authkey=" + msg91_authkey + "&message=" + message
    #     )
    #     if req.status_code == 200:
    #         tempAcc = TempAcc(
    #             toNumber=phone_num,
    #             otp=otp
    #         )
    #         tempAcc.save()
    #         return {"message": "NewUser"}, working
    #     else:
    #         return {"message": "MessageSendingFailed"}, working


def verifyOTP(phone_num, otp, useName=None):
    try:
        tempAcc = TempAcc.objects.get(toNumber=phone_num, otp=otp)
        try:
            cust = Customers(
                userName=tempAcc.username,
                phoneNumber=phone_num,
                referralJoinedFrom=tempAcc.referal
            )
            cust.save()
            token = jwt.encode({
                "user": cust.userName,
                "exp": datetime.utcnow() + timedelta(days=365)
                }, secret_key)
            if tempAcc.referral is not None:
                rewardReferrals(cust.userName, tempAcc.referral)
            return {
                "token": token.decode('UTF-8'),
                "coins": cust.numCoins,
                "referralCode": cust.referralCode
            }, userCreated

        except mongoengine.errors.NotUniqueError:
            cust = Customers.objects.get(userName=tempAcc.username)
            token = jwt.encode({
                "user": cust.userName,
                "exp": datetime.utcnow() + timedelta(days=365)
                }, secret_key)
            return {
                "token": token.decode('UTF-8'),
                "coins": cust.numCoins,
                "referralCode": cust.referralCode
            }, working
    except Exception:
        return {"message": "InvalidOTPEntered"}, working


def rewardReferrals(userName, referee):
    if userName != referee[:-4]:
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
        profilePic = json.loads(
            Customers.objects(
                userName=tokenValidator[0]
            ).only("profilePic").to_json()
        )
        return json.dumps({"data": profilePic}), working


def setPicURL(token, profileURL):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"data": "Login First"}, invalidLoginCredentials
    else:
        try:
            cust = Customers.objects.get(userName=tokenValidator[0])
            cust.update(set__profilePic=profileURL)
            return json.dumps(
                {"data": "ProfilePicUpdated", "url": profileURL}
            ), working
        except Exception:
            return json.dumps({"data": "ProfilePicUpdateFailed"}), working


def getProfileInfo(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Login First"}), invalidLoginCredentials
    else:
        cust = json.loads(
            Customers.objects.get(userName=tokenValidator[0]).to_json()
        )
        stats = {}
        stats["portfolioDays"] = cust["totalPortfolioDays"]
        stats["profitablePortfolioDays"] = cust["totalPortfolioDaysProfitable"]
        stats["quizzesWon"] = cust["quizzesWon"]
        stats["quizzesParticipated"] = cust["quizzesParticipated"]
        stats["questionsAsked"] = cust["questionsAsked"]
        stats["questionsAnswered"] = cust["questionsAnswered"]
        stats["numUpvotes"] = cust["numUpvotes"]
        stats["numberReferrals"] = cust["numberReferrals"]
        stats["userName"] = cust["userName"]
        stats["numCoins"] = cust["numCoins"]
        stats["points_collected"] = cust["cyllidePoints"]
        stats["money_won"] = cust["cashWon"]
        return json.dumps({"data": stats}), working


def getProfileInfoOthers(token, username):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Login First"}), invalidLoginCredentials
    else:
        cust = json.loads(Customers.objects.get(userName=username).to_json())
        stats = {}
        stats["portfolioDays"] = cust["totalPortfolioDays"]
        stats["profitablePortfolioDays"] = cust["totalPortfolioDaysProfitable"]
        stats["quizzesWon"] = cust["quizzesWon"]
        stats["quizzesParticipated"] = cust["quizzesParticipated"]
        stats["questionsAsked"] = cust["questionsAsked"]
        stats["questionsAnswered"] = cust["questionsAnswered"]
        stats["numUpvotes"] = cust["numUpvotes"]
        stats["numberReferrals"] = cust["numberReferrals"]
        stats["userName"] = cust["userName"]
        stats["numCoins"] = cust["numCoins"]
        stats["points_collected"] = cust["cyllidePoints"]
        stats["money_won"] = cust["cashWon"]
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


def checkUsernameValidity(user_name):
    try:
        cust = Customers.objects.get(userName=user_name)
        return json.dumps(
            {
                "status": "taken",
                "suggestion": cust.userName+"123"
            }
        ), working
    except Exception:
        return json.dumps({"status": "available"}), working


# TODO Update Play URL
def homepageInfo(token):
    tokenValidator = validateToken(token)
    # if not tokenValidator[1]:
    #     return json.dumps({"data": "Login First"}), invalidLoginCredentials
    # else:
    cust = json.loads(
        Customers.objects.get(userName=tokenValidator[0]).to_json()
    )
    if cust["cyllidePoints"] <= 1000:
        level = "Bronze"
    elif cust["cyllidePoints"] > 1000 and cust["cyllidePoints"] <= 2000:
        level = "Silver"
    else:
        level = "Gold"
    data = {
        "username": tokenValidator[0],
        "profilePicURL": cust["profilePic"],
        "level": level,
        "version": 1,
        "playurl": "https://google.com",
        "min_withdrawable": 20
    }
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


if __name__ == "__main__":
    from keys import username_db, password_db
    mongoengine.connect(
        db='Cyllide',
        username=username_db,
        password=password_db,
        authentication_source='Cyllide'
    )
    Customers(
        userName="Durgumahanti Prasann",
        phoneNumber=9096332448
    ).save()
