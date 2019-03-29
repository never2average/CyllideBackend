from models import Portfolios, Positions, Customers
import json
from keys import data_encryption_key, secret_key
import jwt
from statuscodes import unAuthorized, working


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
            cust = Customers.objects.get(userName=tokenValidator[0])
            cust.update(add_to_set__portfoliosActiveID=[portfolio.id])
            return json.dumps({"data": "Portfolio Creation Successful"}), working
        except:
            return json.dumps({"data": "Portfolio Creation Failed"}), working


def listMyPortfolios(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        port1 = Portfolios.objects(portfolioOwner=tokenValidator[0]).only("id", "portfolioName", "portfolioCapex")
        return json.dumps({"data": json.loads(port1.to_json())}), working


def listPositions(token, posType="Pending"):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = Portfolios.objects(portfolioOwner=tokenValidator[0], positionsList__state=posType)
        return json.dumps({"data":json.loads(data.to_json())}), working

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
    List = ["smallcap", "midcap", "largecap", "nifty500"]
    count = 0
    for i in List:
        port1 = Portfolios(portfolioOwner="Priyesh",
        portfolioName="Testp"+str(count),
        portfolioCapex=i,
        portfolioStartValue=1000000)
        port1.save()
        count+=1
    for i in List:
        port1 = Portfolios(portfolioOwner="satkriti",
        portfolioName="Testp"+str(count),
        portfolioCapex=i,
        portfolioStartValue=1000000)
        port1.save()
        count+=1
