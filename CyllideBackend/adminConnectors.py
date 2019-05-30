import json
import jwt
import os
from models import Quiz, Questions, Options, Customers, Contests
from models import Portfolios, Content
from statuscodes import unAuthorized, working
from datetime import datetime, timedelta
from dateutil import parser
from keys import admin_secret
from prizeDistribution import calculateEntryFee, heuristic_solution, getReturns


def adminLogin(email, password):
    if (email, password) == ("prasannkumar1263@gmail.com", "prasannkumar1263"):
        token = jwt.encode({
            "user": "prasannkumar1263@gmail.com",
            "exp": datetime.utcnow() + timedelta(hours=24)},
            admin_secret)
        return {"token": token.decode('UTF-8')}, working

    elif (email, password) == ("priyesh.sriv@gmail.com", "adminPassword##123"):
        token = jwt.encode({
            "user": "priyesh.sriv@gmail.com",
            "exp": datetime.utcnow() + timedelta(hours=24)},
            admin_secret)
        return {"token": token.decode('UTF-8')}, working
    else:
        return {"error": "UnsuccessfulLogin"}, unAuthorized


def validateToken(token):
    try:
        email = jwt.decode(token, key=admin_secret)["user"]
        if email == "priyesh.sriv@gmail.com":
            return email,True
        elif email == "prasannkumar1263@gmail.com":
            return True
        else:
            return False
    except Exception:
        return False


def getUserCount(token):
    if validateToken(token):
        return {"numUsers": Customers.objects.count()}, working
    else:
        return {"error": "UnauthorizedRequest"}, unAuthorized


def getQuizHistory(token):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        quizData = json.loads(Quiz.objects().to_json())
        return {"data": quizData}, working


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
        data = json.loads(data)
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
            quizStartTime=parser.parse(data["start_date"]),
            quizQuestions=questionIDList,
            quizPrizeMoney=data["prize_money"]
        )
        newQuiz.save()
        dobj = parser.parse(data["start_date"])
        os.system(
            'aws events put-rule --name "QuizRemoteController_{}_{}_{}_{}" --schedule-expression "cron({} {} {} {} ? {})"'.format(
                dobj.hour, dobj.day, dobj.month, dobj.year, dobj.minute, dobj.hour, dobj.day, dobj.month, dobj.year
            )
        )
        os.system(
            'aws events put-targets --rule QuizRemoteController_{}_{}_{}_{} --targets "Id"="1","Arn"="arn:aws:lambda:ap-south-1:588187310904:function:QuizRemoteControlLambda","Input"={}'.format(
                dobj.hour, dobj.day, dobj.month, dobj.year,json.dumps({"qid":str(newQuiz.id)})
            )
        )
        return {
            "message": "QuizAddedSuccessfully",
            "id": newQuiz.id
            }, working


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
        data = json.loads(data)
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
    soln = heuristic_solution(data["prizePool"], data["capacity"])
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
        ),
        bucketSizeList=soln[1],
        bucketPrizeList=soln[0]
    )
    newContest.save()


def addContent(token, author, title, picURL, articleURL, cType, contentSummary):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        newContent = Content(
            contentAuthor=author,
            contentPic=picURL,
            contentTitle=title,
            contentMarkdownLink=articleURL,
            contentType=cType,
            contentSummary=contentSummary
        )
        newContent.save()
        return {"message": "ContentAddedSuccessfully"}, working


def getContentAnalysis(token):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        return {"data": json.loads(Content.objects.get().to_json())}, working

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
if __name__ == "__main__":
    import mongoengine
    from keys import username_db, password_db
    mongoengine.connect(
        db='Cyllide',
        username=username_db,
        password=password_db,
        authentication_source='admin'
    )
    token = adminLogin("priyesh.sriv@gmail.com", "adminPassword##123")[0]["token"]
    addContent(
        token,
        "Prasann",
        "The Genius of George Soros",
        "https://s3.ap-south-1.amazonaws.com/cyllideassets/soros.jpeg",
        "https://s3.ap-south-1.amazonaws.com/cyllideassets/geniusofgeorgesoros.html",
        "Case Studies",
        'George Soros: One of the most successful yet controversial billionaires in the world. This is the man who nearly robbed UK and made a staggering $1 Billlion of a trade in a single day.'
    )
    addContent(
        token,
        "Prasann",
        "The genius of Mukesh Ambani",
        "https://s3.ap-south-1.amazonaws.com/cyllideassets/ambani.jpeg",
        "https://s3.ap-south-1.amazonaws.com/cyllideassets/mukesh_ambani.html",
        "Case Studies",
        "The story of Jio is no less than a movie plot. Mukeshji always shared a special bond with telecom business. It was his father's dream to start a mobile phone service that would provide voice calls for less than 'the cost of a postcard'."
    )
#mongo -u cyllidedbmanager -p cyllidedbpwd##1
