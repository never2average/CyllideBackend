from models import Customers, Portfolios, Contests, Positions
from keys import secret_key, data_encryption_key
from statuscodes import unAuthorized, working
from simplecrypt import encrypt, decrypt
from datetime import datetime
import json
import random
import jwt
from mongoengine.queryset.visitor import Q


def calculatePret(portfolio):
    return 500 - random.randint(10, 50)


# contestData = {
#     "portfolioUID": "eghfjhbcdnkxsm,z",
#     "contestUID": "fivejwxdnkls"
# }
def enrolPortfolio(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Unauthorized Request"}
        ).encode('utf-8')), unAuthorized
    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        setCon = Contests.objects.get(id=data["contestUID"])
        setCon.update(add_to_set__contestPortfolios=[data["portfolioUID"]])
        return encrypt(data_encryption_key, json.dumps(
            {"message": "PortfolioAddedSuccessfully"}
        ).encode('utf-8')), working


def listAllContests(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Unauthorized Request"}
        ).encode('utf-8')), unAuthorized
    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        contestList = json.loads(
            Contests.objects(
                Q(contestFrequency=data["freq"]) &
                Q(contestEndDate__gte=datetime.now())
                ).to_json()
        )
        return encrypt(data_encryption_key, json.dumps(
            {"message": contestList}
        ).encode('utf-8')), working


def getLeaderBoard(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Unauthorized Request"}
        ).encode('utf-8')), unAuthorized
    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        contestList = json.loads(
            Contests.objects.get(id=data["contestID"]).to_json()
        )
        contestList = contestList["contestPortfolios"]
        portfolioList = []
        for i in contestList:
            portfolioList.append(Portfolios.objects.get(id=i["id"]["$oid"]))
        portfolioList.sort(key=lambda x: calculatePret(x))
        return encrypt(data_encryption_key, json.dumps(
            {"message": portfolioList}
        ).encode('utf-8')), working


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
