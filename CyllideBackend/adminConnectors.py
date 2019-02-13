import json
import jwt
from models import Quiz, Questions, Options, Customers, Contests, Positions
from models import Portfolios, Content
import mongoengine
from statuscodes import unAuthorized, working
from datetime import datetime, timedelta
from dateutil import parser
from keys import admin_secret
from prizeDistribution import calculateEntryFee, heuristic_solution, getReturns
mongoengine.connect('Cyllide')


def adminLogin(email, password):
    if (email, password) == ("prasannkumar1263@gmail.com", "prasannkumar1263"):
        token = jwt.encode({
            "user": "prasannkumar1263@gmail.com",
            "exp": datetime.utcnow() + timedelta(hours=24)},
            adminSecret)
        return {"token": token.decode('UTF-8')}, working

    elif (email, password) == ("priyesh.sriv@gmail.com", "adminPassword##123"):
        token = jwt.encode({
            "user": "priyesh.sriv@gmail.com",
            "exp": datetime.utcnow() + timedelta(hours=24)},
            adminSecret)
        return {"token": token.decode('UTF-8')}, working
    else:
        return {"error": "UnsuccessfulLogin"}, unAuthorized


def validateToken(token):
    try:
        token = json.loads(token)
        email = jwt.decode(token, adminSecret)["user"]
        if email == "priyesh.sriv@gmail.com":
            return True
        elif email == "prasannkumar1263@gmail.com":
            return True
        else:
            return False
    except:
        return False


def getUserCount(token):
    if validateToken(token):
        return {"numUsers": Customers.objects.count()}, working
    else:
        return {"error": "UnauthorizedRequest"}, unAuthorized


def quizHistorian(token):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        return {"data": "valuegoeshere"}, working

"""
quizData = {
    "start_date": "Aug 28 1999 12:00AM",
    "questions":
    [
        {
            "question": "Who the fuck?",
            "options": {"A": 0, "B": 1, "C": 0, "D": 0}
        },
        {
            "question": "Why the fuck?",
            "options": {"A": 0, "B": 0, "C": 1, "D": 0}
        }
    ]
}
"""


def addQuiz(token, data):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        questionIDList = []
        for ind in range(len(data["questions"])):
            i = data["questions"][ind]
            optionList = []
            for j in i["options"].keys():
                optionList.append(Options(
                    value=j,
                    isCorrect=i["options"][j]
                ))

            newques = Questions(
                appearancePosition=ind+1,
                theQuestion=i["question"],
                answerOptions=optionList
            )
            newques.save()
            questionIDList.append(newques.id)

        newQuiz = Quiz(
            quizStartTime=parser.parse(quizData["start_date"]),
            quizQuestions=questionIDList
        )
        newQuiz.save()
        return {"message": "QuizAddedSuccessfully"}, working

"""
contest_data = {
    "name": "Stock Stand-off",
    "frequency": 1,
    "start_date": "Aug 28 1999 12:00AM",
    "isPremium": False,
    "capacity": 20
}

alt_1_contest_data = {
    "name": "Stock Stand-off",
    "frequency": 1,
    "start_date": "Aug 28 1999 12:00AM",
    "isPremium": True,
    "capacity": 2,
    "prizePool": 10000
}
"""


def addContest(token, data):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        if not data["isPremium"]:
            addFreeContest(data)
        else:
            addPaidContest(data)
        return {"message": "ContestAddedSuccessfully"}, working


def addFreeContest(data):
    newContest = Contests(
        contestName=data["name"],
        contestFrequency=data["frequency"],
        contestStartDate=parser.parse(data["start_date"]),
        contestCapacity=data["capacity"]
    )
    newContest.save()


def addPaidContest(data):
    newContest = Contests(
        contestName=data["name"],
        contestFrequency=data["frequency"],
        contestStartDate=parser.parse(data["start_date"]),
        contestCapacity=data["capacity"],
        isPremium=data["isPremium"],
        contestEntryFee=calculateEntryFee(
            data["prizePool"],
            data["capacity"],
            getReturns(data["prizePool"], data["capacity"])
        )
    )
    newContest.save()


def addContent(token, heading, author, title, picURL, articleURL):
    if validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        newContent = Content(
            contentHeading=heading,
            contentAuthor=author,
            contentPic=picURL,
            contentTitle=title,
            contentMarkdownLink=articleURL
        )
        newContent.save()
        return {"message": "ContestAddedSuccessfully"}, working


def getContentAnalysis(token):
    if validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        return {"data": json.loads(Content.objects().to_json())}, working

# addContent(
#     "token", "priyesh", "Priyesh", "Priyesh is Awesome"
#     , "https://google.com", "https://s3.amazonaws.com"
#      )
# print(getContentAnalysis("token"))


def getContestHistory(token):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        data = list(Contests.objects())
        no = Contests.objects.count()
        for i in range(no):
            portfolioList = data[i].contestPortfolios
            m = len(portfolioList)
            for j in range(m):
                portfolioList[i] = json.loads(Portfolios.objects.get(
                    portfolioUID=portfolioList[i]
                    ).to_json())
            data[i].contestPortfolios = portfolioList
            data[i] = json.loads(data[i].to_json())
        return {"data": data}, working

# pos1 = Positions(
#     ticker="AAPL",
#     quantity=10,
#     longPosition=True,
#     entryPrice=123
# )
# pos2 = Positions(
#     ticker="TSLA",
#     quantity=10,
#     longPosition=True,
#     entryPrice=126
# )
# port1 = Portfolios(
#     portfolioUID="ABC_JXNQE",
#     portfolioName="JXNQE",
#     positionsList=[pos1, pos2],
#     portfolioStartValue=working000,
#     cashRemaining=100000
# )
# port1.save()
# con1 = Contests(
#     contestUID="EVCBHWBNJLKMXLSNKM",
#     contestName="Priyesh",
#     contestFrequency=2,
#     contestCapacity=100,
#     contestPortfolios=[port1.portfolioUID],
#     vacancies=100,
#     portfolioStartValue=working000
# )
# con1.save()

# print(getContestHistory("vbdhsdjalsknmldsdvjbdndkm"))
