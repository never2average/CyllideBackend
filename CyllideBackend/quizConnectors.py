from models import Quiz, Questions, Customers
import json
from keys import data_encryption_key, secret_key
import jwt
from statuscodes import unAuthorized, working, limitExceeded
from simplecrypt import encrypt, decrypt
from datetime import datetime
import time


def displayCount(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"data": "Need to login first"}).encode('utf-8')), unAuthorized
    else:
        data = json.loads(decrypt(data_encryption_key, data).decode('utf-8'))
        questionData = json.loads(Questions.objects.get(
            id=data["id"]).to_json())
        return encrypt(data_encryption_key, json.dumps(
            {"data": questionData}).encode('utf-8')), working


def submitAnswer(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"data": "Need to login first"}).encode('utf-8')), unAuthorized
    else:
        data = json.loads(decrypt(data_encryption_key, data).decode('utf-8'))
        questionData = Questions.objects.get(id=data["id"])
        answerList = questionData.answerOptions
        for i in answerList:
            if i.value == data["value"]:
                i.update(set__numResponses=i.numResponses+1)
                questionData.update(set__answerOptions=answerList)
                if i.isCorrect != 0:
                    return encrypt(data_encryption_key, json.dumps(
                        {"data": "Correct"}).encode('utf-8')), working
                else:
                    return encrypt(data_encryption_key, json.dumps(
                        {"data": "Wrong"}).encode('utf-8')), working


def getQuiz(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"data": "Need to login first"}).encode('utf-8')), unAuthorized
    else:
        data = json.loads(decrypt(data_encryption_key, data).decode('utf-8'))
        data = json.loads(Quiz.objects.get(id=data["quizID"]).to_json())
        questionList = data["quizQuestions"]
        for i in range(10):
            questionList[i] = json.loads(
                Questions.objects.get(id=questionList[i]["$oid"]).to_json()
                )
        data["quizQuestions"] = questionList
        return encrypt(data_encryption_key, json.dumps(
            {"data": data}).encode('utf-8')), working


def reviveQuiz(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"data": "Need to login first"}
        )), unAuthorized
    else:
        cust = Customers.objects.get(userName=tokenValidator[0])
        if cust.numCoins <= 0:
            return encrypt(data_encryption_key, json.dumps(
                {"data": "Insufficient Coins"}
            )), limitExceeded
        else:
            cust.update(set__numCoins=cust.numCoins-1)
            return encrypt(data_encryption_key, json.dumps(
                {"data": "Revived Successfully"}
            )), working


def getLatestQuiz(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"data": "Need to login first"}
        )), unAuthorized
    else:
        latestQuiz = Quiz.objects(
            quizStartTime__gte=datetime.now()
            ).order_by('quizStartTime+').first()
        if latestQuiz is not None:
            return encrypt(data_encryption_key, json.dumps(
                {"data": str(latestQuiz.id)}
            )), working
        else:
            return encrypt(data_encryption_key, json.dumps(
                {"data": ""}
            )), working


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


# if __name__ == "__main__":
#     from adminConnectors import adminLogin, addQuiz
#     token = adminLogin(
#         "prasannkumar1263@gmail.com",
#         "prasannkumar1263")[0]["token"]
#     quizData = {
#         "start_date": "Mar 28 2019 12:00AM",
#         "questions":
#         [
#             {
#                 "question": "Who the fuck1?",
#                 "options": {"A": 0, "B": 1, "C": 0, "D": 0}
#             },
#             {
#                 "question": "Why the fuck2?",
#                 "options": {"A": 0, "B": 0, "C": 1, "D": 0}
#             },
#             {
#                 "question": "Who the fuck3?",
#                 "options": {"A": 0, "B": 1, "C": 0, "D": 0}
#             },
#             {
#                 "question": "Why the fuck4?",
#                 "options": {"A": 0, "B": 0, "C": 1, "D": 0}
#             },
#             {
#                 "question": "Who the fuck5?",
#                 "options": {"A": 0, "B": 1, "C": 0, "D": 0}
#             },
#             {
#                 "question": "Why the fuck6?",
#                 "options": {"A": 0, "B": 0, "C": 1, "D": 0}
#             },
#             {
#                 "question": "Who the fuck7?",
#                 "options": {"A": 0, "B": 1, "C": 0, "D": 0}
#             },
#             {
#                 "question": "Why the fuck8?",
#                 "options": {"A": 0, "B": 0, "C": 1, "D": 0}
#             },
#             {
#                 "question": "Who the fuck9?",
#                 "options": {"A": 0, "B": 1, "C": 0, "D": 0}
#             },
#             {
#                 "question": "Why the fuck10?",
#                 "options": {"A": 0, "B": 0, "C": 1, "D": 0}
#             }
#         ]
#     }
#     quizData = json.dumps(quizData)
#     dummyQuiz = addQuiz(token, quizData)[0]
#     dummyQuiz = {"quizID": str(dummyQuiz["id"])}
#     print(getLatestQuiz("token"))