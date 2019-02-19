from models import Quiz, Questions, Customers
import json
from keys import data_encryption_key, secret_key
import jwt
from datetime import datetime, timedelta
from statuscodes import unAuthorized, working
from simplecrypt import encrypt, decrypt


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


def validateToken(token):
    try:
        username = jwt.decode(token, secret_key)["user"]
        try:
            cust = Customers.objects.get(userName=username)
            return cust.userName, True
        except:
            return None, False
    except:
        return None, False
