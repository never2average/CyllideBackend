from models import Customers, Portfolios, Contests, Notifications
from keys import secret_key
from statuscodes import unAuthorized, working
import json
import random
import jwt
from mongoengine.queryset.visitor import Q
import datetime


def calculatePret(portfolio):
    return (500 - random.randint(0, 1000))/5


# contestData = {
#     "portfolioUID": "eghfjhbcdnkxsm,z",
#     "contestUID": "fivejwxdnkls"
# }
def enrolPortfolio(token, contestUID, portfolioUID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"message": "Unauthorized Request"}
        ), unAuthorized
    else:
        setCon = Contests.objects.get(id=contestUID)
        portfolioOwners = [i.portfolioOwner for i in setCon.contestPortfolios]
        if portfolioUID not in portfolioOwners:
            setCon.update(add_to_set__contestPortfolios=[portfolioUID])
            cust = Customers.objects.get(userName=tokenValidator[0])
            cust.update(add_to_set__contestsActiveID=[setCon.id])
            setCon.update(inc__signUps=1)
            notification = Notifications(
                username=tokenValidator[0],
                message="Your portfolio has been enrolled into the contest",
                notificationTime=datetime.now()
            )
            notification.save()
            return json.dumps(
                {"message": "PortfolioAddedSuccessfully"}
            ), working
        else:
            return json.dumps(
                {"message": "PortfolioAlreadyRegistered"}
            ), working


def listAllContests(token, capex):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"message": "Unauthorized Request"}), unAuthorized
    else:
        contestList = json.loads(
            Contests.objects(
                contestCapex=capex
            ).only("id", "contestCapex", "signUps").to_json()
        )
        cust = Customers.objects.get(userName=tokenValidator[0])
        cust = json.loads(cust.to_json())["contestsActiveID"]
        for i in contestList:
            if i["_id"] in cust:
                i["isAlreadyIn"] = True
                break
        else:
            i["isAlreadyIn"] = False
        return json.dumps({"message": contestList}), working


def getLeaderBoard(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"message": "Unauthorized Request"}), unAuthorized
    else:
        leaderboard = Customers.objects.only(
            "id","userName","profilePic","numStreaks", "numDaysCurrentStreak", "userLevel"
        ).order_by("-numStreaks", "-numDaysCurrentStreak")
        leaderboard = json.loads(leaderboard.to_json())
        for i in leaderboard:
            i["isTrue"] = (i["userName"] == tokenValidator[0])
            if not i["isTrue"]:
                del i["numDaysCurrentStreak"]
                del i["userLevel"]
        return json.dumps({"leaderboard": leaderboard}), working


def listRelevantPortfolios(token, capex):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"message": "Unauthorized Request"}
        ), unAuthorized
    else:
        portfolioList = Portfolios.objects(
            Q(portfolioOwner=tokenValidator[0]) &
            Q(portfolioCapex=capex)
            ).only("id", "portfolioName")
        portfolioList = json.loads(portfolioList.to_json())
        return {"data": portfolioList}, working


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
    from keys import username_db, password_db
    mongoengine.connect(
        db='Cyllide',
        username=username_db,
        password=password_db,
        authentication_source='admin'
    )
    # List = ["smallcap","largecap","midcap","nifty500"]
    # for i in List:
    #     list1 = Contests(contestName = i+"trial",contestCapex=i)
    #     list1.save()
    contest1 = Contests(contestName="Nifty500 Royale", contestCapex="nifty500")
    contest1.save()
    # port1 = Portfolios(
    #     portfolioOwner="None",
    #     portfolioName="portrt1",
    #     portfolioCapex="smallcap"
    #     )
    # port1.save()
    # cust1 = Customers(userName="None", phoneNumber=9773065091)
    # cust1.save()
    # print(enrolPortfolio("wwdkjsqlnkm", contest1.id, port1.id))
