import json
import jwt
import os
from models import Quiz, Questions, Options, Customers
from models import Content
from statuscodes import unAuthorized, working, processFailed
from datetime import datetime, timedelta
from dateutil import parser
from keys import admin_secret


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
            return email, True
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
        dobj -= timedelta(minutes=330)
        os.system(
            'aws events put-rule --name "QuizRemoteController_{}_{}_{}_{}_{}" --description "Activates the remote controller for the Quiz" --schedule-expression "cron({} {} {} {} ? {})"'.format(
                dobj.minute, dobj.hour, dobj.day, dobj.month, dobj.year,
                dobj.minute, dobj.hour, dobj.day, dobj.month, dobj.year
            )
        )
        os.system(
            "aws lambda add-permission --function-name QuizRemoteControlLambda --action 'lambda:InvokeFunction' --principal events.amazonaws.com --statement-id my-event-{}-{}-{}-{}-{} --source-arn arn:aws:events:ap-south-1:588187310904:rule/QuizRemoteController_{}_{}_{}_{}_{}".format(
                dobj.minute, dobj.hour, dobj.day, dobj.month, dobj.year,
                dobj.minute, dobj.hour, dobj.day, dobj.month, dobj.year
            )
        )
        os.system(
            'aws events put-targets --rule QuizRemoteController_{}_{}_{}_{}_{} --targets "Id"="1","Arn"="arn:aws:lambda:ap-south-1:588187310904:function:QuizRemoteControlLambda"'.format(
                dobj.minute, dobj.hour, dobj.day, dobj.month, dobj.year
            )
        )
        return {
            "message": "QuizAddedSuccessfully",
            "id": newQuiz.id
        }, working


def addContent(
    token, author,
    title, picURL,
    articleURL, cType,
    contentSummary
):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        tags = {
            "Case Studies": "#FAFA8F",
            "Legends of the Game": "#6F58C9",
            "Stories": "#5E8C61"
        }
        newContent = Content(
            contentAuthor=author,
            contentPic=picURL,
            contentTitle=title,
            contentMarkdownLink=articleURL,
            contentType=cType,
            contentSummary=contentSummary,
            contentColor=tags[cType]
        )
        newContent.save()
        return {"message": "ContentAddedSuccessfully"}, working


def getContentAnalysis(token):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        return {"data": json.loads(Content.objects.get().to_json())}, working


def inshortsAdder(token, content):
    if not validateToken(token):
        return {"error": "UnauthorizedRequest"}, unAuthorized
    else:
        try:
            for i in content:
                Content(
                    title=i["title"],
                    imageURL=i["url"],
                    description=i["description"]
                ).save()
            return {"message": "ContentAdditionSuccessful"}, working
        except Exception:
            return {"message": "ContentAdditionFailed"}, processFailed

# if __name__ == "__main__":
#     import mongoengine
#     from keys import username_db, password_db
#     mongoengine.connect(
#         db='Cyllide',
#         username=username_db,
#         password=password_db,
#         authentication_source='admin'
#     )
#     token = adminLogin(
#         "priyesh.sriv@gmail.com",
#         "adminPassword##123"
#     )[0]["token"]
#     addContent(
#         token,
#         "Prasann",
#         "The Genius of George Soros",
#         "https://s3.ap-south-1.amazonaws.com/cyllideassets/soros.jpeg",
#         "https://s3.ap-south-1.amazonaws.com/cyllideassets/geniusofgeorgesoros.html",
#         "Case Studies",
#         'George Soros: One of the most successful yet controversial billionaires in the world. This is the man who nearly robbed UK and made a staggering $1 Billlion of a trade in a single day.'
#     )
#     addContent(
#         token,
#         "Prasann",
#         "The genius of Mukesh Ambani",
#         "https://s3.ap-south-1.amazonaws.com/cyllideassets/ambani.jpeg",
#         "https://s3.ap-south-1.amazonaws.com/cyllideassets/mukesh_ambani.html",
#         "Case Studies",
#         "The story of Jio is no less than a movie plot. Mukeshji always shared a special bond with telecom business. It was his father's dream to start a mobile phone service that would provide voice calls for less than 'the cost of a postcard'."
#     )
# mongo -u cyllidedbmanager -p cyllidedbpwd##1
