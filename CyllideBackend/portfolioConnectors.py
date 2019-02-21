from models import Portfolios, Positions, Customers
import json
from keys import data_encryption_key, secret_key
import jwt
from datetime import datetime, timedelta
from statuscodes import unAuthorized, working
from simplecrypt import encrypt, decrypt

examplePortfolio = {
    "positions": [
        {
            "entryTime": 1550393725,
            "ticker": "INFY",
            "quantity": 200,
            "longPosition": True
        }
    ],
    "portfolioName": "portfolio123",
    "portfolioStartValue": 200000,
    "cashRemaining": 100000
}


def storePortfolios(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(
            data_encryption_key, json.dumps(
                {"data": "Need to login first"}).encode('utf-8')), unAuthorized
    else:
        data = json.loads(decrypt(data_encryption_key, data).decode('utf-8'))
        positionList = []

        for i in data["positions"]:
            pos = Positions(
                entryTime=datetime.utcfromtimestamp(i["entryTime"]).strftime(
                    '%Y-%m-%d %H:%M:%S')+timedelta(minutes=330),
                ticker=i["ticker"],
                quantity=i["quantity"],
                longPosition=i["longPosition"]
            )
            positionList.append(pos)

        portfolio = Portfolios(
            portfolioUID=data[
                "portfolioName"]+token[0]+datetime.now().timestamp(),
            portfolioName=data["portfolioName"],
            positionsList=positionList,
            portfolioStartValue=data["portfolioStartValue"],
            cashRemaining=data["cashRemaining"]
        )
        portfolio.save()
        cust = Customers.objects.get(userName=tokenValidator[0])
        cust.update(add_to_set__portfoliosActiveID=[portfolio.id])
        return encrypt(data_encryption_key, json.dumps(
            {"data": "Portfolio Stored Successfully"}
            ).encode('utf-8')), working


def listMyPortfolios(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"data": "Need to login first"}).encode('utf-8')
            ), unAuthorized
    else:
        portfolioNameList = {}
        cust = Customers.objects.get(userName=tokenValidator[0])
        for i in list(cust.portfoliosActiveID):
            portfolioNameList[i.id] = i.portfolioName
        return encrypt(data_encryption_key, json.dumps(
            {"data": portfolioNameList}
            ).encode('utf-8')), working


def listSpecificPortfolios(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"data": "Need to login first"}
            ).encode('utf-8')), unAuthorized
    else:
        data = json.loads(decrypt(data_encryption_key, data).decode('utf-8'))
        portfolioData = Portfolios.objects.get(id=data[pid]).to_json()
        return encrypt(data_encryption_key, json.dumps(
            {"data": portfolioData}).encode('utf-8')), working


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
