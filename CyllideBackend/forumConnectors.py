from models import Customers, Query, Answer, Comment
from keys import secret_key, data_encryption_key
from simplecrypt import encrypt, decrypt
from statuscodes import unAuthorized, accepted
from datetime import datetime
import json
import jwt
import mongoengine
mongoengine.connect('Cyllide')


def addQuery(token, queryBody, *tags):
    tokenValidator = validateToken(token)
    queryBody = decrypt(data_encryption_key, queryBody).decode('utf-8')
    if not tokenValidator[1]:
        return encrypt(
            data_encryption_key,
            json.dumps(
                {"message": "Could Not Post Question"}
                ).encode('utf-8')), unAuthorized
    else:
        newQuery = Query(
            queryUID=tokenValidator[0],
            queryBody=queryBody,
            queryTags=tags
            )
        newQuery.save()
        return encrypt(data_encryption_key, json.dumps({
            "message": "Question Posted Successfully",
            "ID": newQuery.id
            }).encode('utf-8')), accepted


def editQuery(token, qid, queryBodyNew, *queryTagsNew):
    qid = decrypt(data_encryption_key, qid).decode('utf-8')
    queryBodyNew = decrypt(data_encryption_key, queryBodyNew).decode('utf-8')
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"})
            .encode('utf-8')), unAuthorized
    else:
        newQuery = Query.objects.get(id=qid)
        newQuery.update(set__queryBody=queryBodyNew)
        newQuery.update(set__queryLastUpdateTime=datetime.now())
        newQuery.update(set__queryTags=queryTagsNew)
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Question Edited Successfully"}
            ).encode('utf-8')), accepted


def upvoteQuery(token, qid):
    tokenValidator = validateToken(token)
    qid = decrypt(data_encryption_key, qid).decode('utf-8')
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"})
            .encode('utf-8')), unAuthorized
    else:
        newQuery = Query.objects.get(id=qid)
        newQuery.update(set__queryUpvotes=newQuery.queryUpvotes+1)
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Question Upvoted Successfully"}
        ).encode('utf-8')), accepted


def addAnswer(token, qid, answerBody):
    tokenValidator = validateToken(token)
    qid = decrypt(data_encryption_key, qid).decode('utf-8')
    answerBody = decrypt(data_encryption_key, answerBody).decode('utf-8')
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"}
        ).encode('utf-8')), unAuthorized
    else:
        newAnswer = Answer(
            answerUID=tokenValidator[0],
            answerBody=answerBody
            )
        newAnswer.save()
        print(newAnswer.answerBody)
        newQuery = Query.objects.get(id=qid)
        newQuery.update(add_to_set__answerList=[newAnswer.id])
        newQuery.update(set__isAnswered=True)
        return encrypt(data_encryption_key, json.dumps({
            "message": "Answer Posted Successfully",
            "ID": newAnswer.id
            }).encode('utf-8')), accepted


def makeComment(token, qid, commentBody):
    tokenValidator = validateToken(token)
    qid = decrypt(data_encryption_key, qid).decode('utf-8')
    commentBody = decrypt(data_encryption_key, commentBody).decode('utf-8')
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"}
        ).encode('utf-8')), unAuthorized

    else:
        newComment = Comment(
            commentUID=tokenValidator[0],
            commentBody=commentBody
            )
        newQuery = Query.objects.get(id=qid)
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
            {"message": json.loads(Query.objects.to_json())}
        ).encode('utf-8')), accepted


def displayOneQuery(token, qid):
    qid = decrypt(data_encryption_key, qid).decode('utf-8')
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"}
        ).encode('utf-8')), unAuthorized
    else:
        newQuery = Query.objects.get(id=qid)
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


def upvoteAnswer(token, aid):
    tokenValidator = validateToken(token)
    aid = decrypt(data_encryption_key, aid).decode('utf-8')
    if not tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Could Not Post Question"}
        ).encode('utf-8')), unAuthorized
    else:
        newAnswer = Answer.objects.get(id=aid)
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
