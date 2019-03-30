from models import Portfolios, Positions, Customers
import json
from keys import data_encryption_key, secret_key
import jwt
from statuscodes import unAuthorized, working
from datetime import datetime, timedelta
from mongoengine.queryset.visitor import Q


def makePortfolios(token, name, capex):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        try:
            portfolio = Portfolios(
                portfolioName=name,
                portfolioOwner=tokenValidator[0],
                portfolioCapex=capex
                )
            portfolio.save()
            portfolio = json.loads(portfolio.to_json())
            cust = Customers.objects.get(userName=tokenValidator[0])
            cust.update(add_to_set__portfoliosActiveID=portfolio["_id"]["$oid"])
            return json.dumps({"data": "Portfolio Creation Successful","id": portfolio["_id"]["$oid"]}), working
        except Exception:
            return json.dumps({"data": "Portfolio Creation Failed"}), working


def listMyPortfolios(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        port1 = Portfolios.objects(portfolioOwner=tokenValidator[0]).only("id", "portfolioName", "portfolioCapex")
        return json.dumps({"data": json.loads(port1.to_json())}), working


def listPositions(token, portfolioID, posType="Pending"):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = Portfolios.objects.get(id=portfolioID)
        data = json.loads(data.to_json())
        print(data)
        return json.dumps({"data":[i for i in data["positionsList"] if i["state"]==posType]}), working


def takePosition(token, portfolioID, ticker, quantity, isLong):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = Portfolios.object.get(id=portfolioID)
        if isLong == "LONG":
            pos = Positions(
                ticker=ticker,
                quantity=int(quantity),
                longPosition=True)
        else:
            pos = Positions(
                ticker=ticker,
                quantity=int(quantity),
                longPosition=False)
        data.update(add_to_set__positionsList=[pos])
        return json.dumps({"data":"Order Placed"}), working


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

if __name__ == "__main__":
    import mongoengine
    mongoengine.connect("Cyllide")
    pos=[]
    l = ["Pending","Holding", "Closed","Holding", "Closed", "Pending", "Holding"]
    for i in l:
        if i=="Pending":
            pos.append(
                Positions(ticker="RELIANCE", quantity=10, longPosition=True, state=i)
            )
        elif i=="Holding":
            pos.append(
                Positions(
                    ticker="RELIANCE", quantity=10, longPosition=True, state=i, entryPrice=12.34,
                    entryTime=datetime.now()
                )
            )
        else:
            pos.append(
                Positions(
                    ticker="RELIANCE", quantity=10, longPosition=True, state=i, entryPrice=12.34,
                    exitPrice=13.42, entryTime=datetime.now(),
                    exitTime=datetime.now()+timedelta(hours=15)
                )
            )
    capexes = ["smallcap", "largecap", "midcap", "nifty500"]
    count = 0
    for j in capexes:
        port1 = Portfolios(portfolioOwner="Priyesh",
            portfolioName="Testp"+str(count),
            portfolioCapex=j,
            portfolioStartValue=1000000,
            positionsList=pos)
        port1.save()
        count+=1
    # List = ["smallcap", "midcap", "largecap", "nifty500"]
    # count = 0
    # for i in List:
    #     port1 = Portfolios(portfolioOwner="Priyesh",
    #     portfolioName="Testp"+str(count),
    #     portfolioCapex=i,
    #     portfolioStartValue=1000000)
    #     port1.save()
    #     count+=1
    # for i in List:
    #     port1 = Portfolios(portfolioOwner="satkriti",
    #     portfolioName="Testp"+str(count),
    #     portfolioCapex=i,
    #     portfolioStartValue=1000000)
    #     port1.save()
    #     count+=1