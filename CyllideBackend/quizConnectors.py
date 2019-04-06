from models import Quiz, Questions, Customers, Award
import json
from keys import secret_key
import jwt
from statuscodes import unAuthorized, working, limitExceeded
from datetime import datetime


def displayCount(token, questionID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        questionData = json.loads(Questions.objects.get(
            id=questionID).to_json())
        return json.dumps({"data": questionData["numResponses"]}), working


def submitAnswer(token, questionID, optionValue):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        questionData = Questions.objects.get(id=questionID)
        answerList = questionData.answerOptions
        for i in answerList:
            if i.value == optionValue:
                if i.isCorrect != 0:
                    to_inc = dict(inc__answerOptions__S__numResponses=1, inc__numResponses=1, inc__numSuccessfulResponses=1)
                    Questions.objects(id=questionID, answerOptions__value=i.value).update(**to_inc)
                    return json.dumps({"data": "Correct"}), working
                else:
                    to_inc = dict(inc__answerOptions__S__numResponses=1, inc__numResponses=1)
                    Questions.objects(id=questionID, answerOptions__value=i.value).update(**to_inc)
                    return json.dumps({"data": "Wrong"}), working
        to_inc = dict(inc__answerOptions__S__numResponses=1, inc__numResponses=1)
        Questions.objects(id=questionID, answerOptions__value=i.value).update(**to_inc)
        return json.dumps({"data": "Wrong"}), working


def getQuiz(token, quizID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        data = json.loads(Quiz.objects.get(id=quizID).to_json())
        questionList = data["quizQuestions"]
        for i in range(10):
            questionList[i] = json.loads(
                Questions.objects.get(id=questionList[i]["$oid"]).to_json()
                )
        return json.dumps({"data": questionList}), working


def quizStats(token, questionID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        quest = Questions.objects(id=questionID).only("id","answerOptions").to_json()
        return json.dumps({"data":json.loads(quest)}), working


def reviveQuiz(token, numCoins, questionID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        to_inc = dict(inc__numResponses=1, inc__numSuccessfulResponses=1)
        Questions.objects(id=questionID).update(**to_inc)
        Customers.objects(userName=tokenValidator[0]).update(set__numCoins=numCoins)
        return json.dumps(
            {"data": "Coins Updated"}
        ), working


def getLatestQuiz(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        latestQuiz = Quiz.objects(quizStartTime__gte=datetime.now()).order_by('quizStartTime').only("id","quizStartTime").exclude('quizQuestions', "quizWinners", "quizParticipants").first().to_json()
        if latestQuiz is not None:
            return json.dumps({"data": json.loads(latestQuiz)}), working
        else:
            return json.dumps({"data": ""}), working


def numProceeders(token, questionID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        return json.dumps(
            {"data": json.loads(Questions.objects(id=questionID).only("id", "numSuccessfulResponses").to_json())}
        ), working


def quizRewards(token, quizID, upiID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        try:
            cust = Customers.objects.get(userName=username)
            cust.update(inc__quizzesWon=1)
            quiz = Quiz.objects.get(id=quizID)
            aw = Award(quizID=quiz.id,username=tokenValidator[0],UPI=upiID)
            aw.save()
        except Exception:
            return json.dumps({"data": "InvalidQuizID"}), unAuthorized


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
    from adminConnectors import adminLogin, addQuiz
    token = adminLogin(
        "prasannkumar1263@gmail.com",
        "prasannkumar1263")[0]["token"]
    quizData = {
        "start_date": "Mar 30 2020 8:00AM",
        "questions":
        [
            {
                "question": "Who the fuck1?",
                "options": {"1A": 0, "1B": 1, "1C": 0, "1D": 0}
            },
            {
                "question": "Why the fuck2?",
                "options": {"2A": 0, "2B": 0, "2C": 1, "2D": 0}
            },
            {
                "question": "Who the fuck3?",
                "options": {"3A": 0, "3B": 1, "3C": 0, "3D": 0}
            },
            {
                "question": "Why the fuck4?",
                "options": {"4A": 0, "4B": 0, "4C": 1, "4D": 0}
            },
            {
                "question": "Who the fuck5?",
                "options": {"5A": 0, "5B": 1, "5C": 0, "5D": 0}
            },
            {
                "question": "Why the fuck6?",
                "options": {"6A": 0, "6B": 0, "6C": 1, "6D": 0}
            },
            {
                "question": "Who the fuck7?",
                "options": {"7A": 0, "7B": 1, "7C": 0, "7D": 0}
            },
            {
                "question": "Why the fuck8?",
                "options": {"8A": 0, "8B": 0, "8C": 1, "8D": 0}
            },
            {
                "question": "Who the fuck9?",
                "options": {"9A": 0, "9B": 1, "9C": 0, "9D": 0}
            },
            {
                "question": "Why the fuck10?",
                "options": {"10A": 0, "10B": 0, "10C": 1, "10D": 0}
            }
        ]
    }
    quizData = json.dumps(quizData)
    dummyQuiz = addQuiz(token, quizData)
