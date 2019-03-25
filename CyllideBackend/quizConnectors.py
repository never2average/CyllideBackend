from models import Quiz, Questions, Customers
import json
from keys import data_encryption_key, secret_key
import jwt
from statuscodes import unAuthorized, working, limitExceeded
from simplecrypt import encrypt, decrypt
from datetime import datetime


def displayCount(token, questionID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        questionData = json.loads(Questions.objects.get(
            id=questionID).only("numResponses").to_json())
        return json.dumps({"data": questionData}), working


def submitAnswer(token, questionID, optionValue):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        questionData = Questions.objects.get(id=questionID)
        answerList = questionData.answerOptions
        for i in answerList:
            if i.value == optionValue:
                i.update(set__numResponses=i.numResponses+1)
                questionData.update(set__answerOptions=answerList)
                if i.isCorrect != 0:
                    return json.dumps({"data": "Correct"}), working
                else:
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
        data["quizQuestions"] = questionList
        return json.dumps({"data": data}), working


def reviveQuiz(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        cust = Customers.objects.get(userName=tokenValidator[0])
        if cust.numCoins <= 0:
            return json.dumps(
                {"data": "Insufficient Coins"}
            ), limitExceeded
        else:
            cust.update(set__numCoins=cust.numCoins-1)
            return json.dumps(
                {"data": "Revived Successfully"}
            ), working


def getLatestQuiz(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        latestQuiz = Quiz.objects(quizStartTime__gte=datetime.now()
            ).order_by('quizStartTime-').only("id","quizStartTime").exclude('quizQuestions', "quizWinners", "quizParticipants").first().to_json()
        if latestQuiz is not None:
            return json.dumps({"data": json.loads(latestQuiz)}), working
        else:
            return json.dumps({"data": ""}), working


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
        "start_date": "Mar 26 2019 11:50PM",
        "questions":
        [
            {
                "question": "Who the fuck1?",
                "options": {"A": 0, "B": 1, "C": 0, "D": 0}
            },
            {
                "question": "Why the fuck2?",
                "options": {"A": 0, "B": 0, "C": 1, "D": 0}
            },
            {
                "question": "Who the fuck3?",
                "options": {"A": 0, "B": 1, "C": 0, "D": 0}
            },
            {
                "question": "Why the fuck4?",
                "options": {"A": 0, "B": 0, "C": 1, "D": 0}
            },
            {
                "question": "Who the fuck5?",
                "options": {"A": 0, "B": 1, "C": 0, "D": 0}
            },
            {
                "question": "Why the fuck6?",
                "options": {"A": 0, "B": 0, "C": 1, "D": 0}
            },
            {
                "question": "Who the fuck7?",
                "options": {"A": 0, "B": 1, "C": 0, "D": 0}
            },
            {
                "question": "Why the fuck8?",
                "options": {"A": 0, "B": 0, "C": 1, "D": 0}
            },
            {
                "question": "Who the fuck9?",
                "options": {"A": 0, "B": 1, "C": 0, "D": 0}
            },
            {
                "question": "Why the fuck10?",
                "options": {"A": 0, "B": 0, "C": 1, "D": 0}
            }
        ]
    }
    quizData = json.dumps(quizData)
    dummyQuiz = addQuiz(token, quizData)
