from models import Customers, Query, Answer, Comment
from keys import secret_key, data_encryption_key
from simplecrypt import encrypt, decrypt
from statuscodes import unAuthorized, accepted
from datetime import datetime
import json
import jwt
import mongoengine
mongoengine.connect('Cyllide')


def addQuery(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(
            data_encryption_key,
            json.dumps(
                {"message": "Could Not Post Question"}
                ).encode('utf-8')), unAuthorized
    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        newQuery = Query(
            queryUID=tokenValidator[0],
            queryBody=data["queryBody"],
            queryTags=data["tags"]
            )
        newQuery.save()
        return encrypt(data_encryption_key, json.dumps({
            "message": "Question Posted Successfully",
            "ID": newQuery.id
            }).encode('utf-8')), accepted


def editQuery(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"})
            .encode('utf-8')), unAuthorized
    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        newQuery = Query.objects.get(id=data["qid"])
        newQuery.update(set__queryBody=data["queryBodyNew"])
        newQuery.update(set__queryLastUpdateTime=datetime.now())
        newQuery.update(set__queryTags=data["queryTagsNew"])
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Question Edited Successfully"}
            ).encode('utf-8')), accepted


def upvoteQuery(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"})
            .encode('utf-8')), unAuthorized
    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        newQuery = Query.objects.get(id=data["qid"])
        newQuery.update(set__queryUpvotes=newQuery.queryUpvotes+1)
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Question Upvoted Successfully"}
        ).encode('utf-8')), accepted


def addAnswer(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"}
        ).encode('utf-8')), unAuthorized
    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        newAnswer = Answer(
            answerUID=tokenValidator[0],
            answerBody=data["answerBody"]
            )
        newAnswer.save()
        newQuery = Query.objects.get(id=data["qid"])
        newQuery.update(add_to_set__answerList=[newAnswer.id])
        newQuery.update(set__isAnswered=True)
        return encrypt(data_encryption_key, json.dumps({
            "message": "Answer Posted Successfully",
            "ID": newAnswer.id
            }).encode('utf-8')), accepted


def makeComment(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"}
        ).encode('utf-8')), unAuthorized

    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        newComment = Comment(
            commentUID=tokenValidator[0],
            commentBody=data["commentBody"]
            )
        newQuery = Query.objects.get(id=data["qid"])
        newQuery.update(add_to_set__commentList=[newComment])
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Comment Posted Successfully"}
        ).encode('utf-8')), accepted


def displayAllQueries(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"}
        ).encode('utf-8')), unAuthorized
    else:
        return encrypt(data_encryption_key, json.dumps(
            {"message": json.loads(Query.objects().to_json())}
        ).encode('utf-8')), accepted


def displayOneQuery(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"}
        ).encode('utf-8')), unAuthorized
    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        newQuery = Query.objects.get(id=data["qid"])
        newQuery = json.loads(newQuery.to_json())
        ansList = newQuery['answerList']
        ansListNew = []
        for i in ansList:
            newAns = Answer.objects.get(id=list(i.values())[0])
            ansListNew.append(json.loads(newAns.to_json()))
        newAns['answerList'] = ansListNew
        return encrypt(data_encryption_key, json.dumps(
            {"message": newAns}
        ).encode('utf-8')), accepted


def upvoteAnswer(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"}
        ).encode('utf-8')), unAuthorized
    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        newAnswer = Answer.objects.get(id=data["aid"])
        newAnswer.update(set__answerUpvotes=newAnswer.answerUpvotes+1)
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Answer Upvoted Successfully"}
        ).encode('utf-8')), accepted


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

# TODO Phone Authentication required
