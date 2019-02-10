import json
import jwt
from models import Quiz, Questions, Options, Customers, Contests

import mongoengine
from datetime import datetime, timedelta
from dateutil import parser
from prizeDistribution import calculateEntryFee, heuristic_solution, getReturns
mongoengine.connect('Cyllide')
adminSecret = "vyuewgqfhscjkwlsbfvhdwkjakxmsnxjksdvfdjskaxm,"


def adminLogin(email, password):
    if (email, password) == ("prasannkumar1263@gmail.com", "prasannkumar1263"):
        token = jwt.encode({
            "user": "prasannkumar1263@gmail.com",
            "exp": datetime.utcnow() + timedelta(hours=24)},
            adminSecret)
        return {"token": token.decode('UTF-8')}, 200

    elif (email, password) == ("priyesh.sriv@gmail.com", "adminPassword##123"):
        token = jwt.encode({
            "user": "priyesh.sriv@gmail.com",
            "exp": datetime.utcnow() + timedelta(hours=24)},
            adminSecret)
        return {"token": token.decode('UTF-8')}, 200
    else:
        return {"error": "UnsuccessfulLogin"}, 301


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
        return {"numUsers": Customers.objects.count()}, 200
    else:
        return {"error": "UnauthorizedRequest"}, 401


def quizHistorian(token):
    if validateToken(token):
        return {"data": "valuegoeshere"}, 200
    else:
        return {"error": "UnauthorizedRequest"}, 401

"""
quizData = {
    "start_date": "Aug 28 1999 12:00AM",
    "questions":
    [
        {
            "question": "Why the fuck?",
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
        return {"error": "UnauthorizedRequest"}, 401
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
        return {"message": "QuizAddedSuccessfully"}, 200

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
        return {"error": "UnauthorizedRequest"}, 401
    else:
        if not data["isPremium"]:
            addFreeContest(data)
        else:
            addPaidContest(data)
        return {"message": "ContestAddedSuccessfully"}, 200


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
        contestEntryFee=calculateEntryFee(data["prizePool"], data["capacity"], getReturns(data["prizePool"], data["capacity"]))
    )
    newContest.save()


def addContent(token, email, author, title, picURL, articleURL):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, 401
    else:
        newContent = Content(
            contentHeading=email,
            contentAuthor=author,
            contentPic=picURL,
            contentTitle=title,
            contentMarkdownLink=articleURL
        )
        newContent.save()
        return {"message": "ContestAddedSuccessfully"}, 200


def getContentAnalysis(token):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, 401
    else:
        return {"data": Contests.objects.get().to_json()}, 200

