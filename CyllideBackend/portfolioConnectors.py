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
            portfolio.update(set__portfolioProfilePic=cust.profilePic)
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
        portfolioList = [i for i in data["positionsList"] if i["state"]==posType]
        if posType == "Closed":
            portfolioList.sort(key=lambda x: x["exitTime"]["$date"])
            portfolioList.reverse()
        return json.dumps({"data":portfolioList}), working


def takePosition(token, portfolioID, ticker, quantity, isLong):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = Portfolios.objects.get(id=portfolioID)
        if isLong == "LONG":
            pos = Positions(
                ticker=ticker,
                quantity=int(quantity),
                longPosition=True,
                entryTime=datetime.now())
        else:
            pos = Positions(
                ticker=ticker,
                quantity=int(quantity),
                longPosition=False,
                entryTime=datetime.now())
        data.update(add_to_set__positionsList=[pos])
        return json.dumps({"data":"Order Placed"}), working


def deletePosition(token, portfolioID, state, ticker, quantity, isLong):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        if isLong == "LONG":
            isLong = True
        else:
            isLong = False
        data = Portfolios.objects.get(id=portfolioID)
        ll = data.positionsList
        n = len(ll)
        for i in range(n):
            if ll[i].state==state and ll[i].ticker==ticker and ll[i].longPosition==isLong and ll[i].quantity==int(quantity):
                if ll[i].state == "Pending":
                    ll.pop(i)
                    break
                elif ll[i].state == "Holding":
                    ll.append(Positions(
                        ticker=ll[i].ticker,
                        quantity=ll[i].quantity,
                        longPosition=not isLong,
                        entryTime=datetime.now())
                    )
                    ll.pop(i)
                    break

        data.update(set__positionsList=ll)
        return json.dumps({"data":[json.loads(i.to_json()) for i in ll]}), working



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
    pos = []
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