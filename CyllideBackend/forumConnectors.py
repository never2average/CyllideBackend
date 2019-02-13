from models import Customers, Query, Answer, Comment
from keys import secret_key
from statuscodes import unAuthorized, working, accepted, processFailed
from datetime import datetime
import json
import mongoengine
mongoengine.connect('Cyllide')


def addQuery(token, queryBody, *tags):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"message": "Could Not Post Question"}, unAuthorized
    else:
        newQuery = Query(
            queryUID=tokenValidator[0],
            queryBody=queryBody,
            queryTags=tags
            )
        newQuery.save()
        return {
            "message": "Question Posted Successfully",
            "ID": newQuery.id
            }, accepted


def editQuery(token, qid, queryBodyNew, *queryTagsNew):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"message": "Could Not Post Question"}, unAuthorized
    else:
        newQuery = Query.objects.get(id=qid)
        newQuery.update(set__queryBody=queryBodyNew)
        newQuery.update(set__queryLastUpdateTime=datetime.now())
        newQuery.update(set__queryTags=queryTagsNew)
        return {"message": "Question Edited Successfully"}, accepted


def upvoteQuery(token, qid):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"message": "Could Not Post Question"}, unAuthorized
    else:
        newQuery = Query.objects.get(id=qid)
        newQuery.update(set__queryUpvotes=newQuery.queryUpvotes+1)
        return {"message": "Question Upvoted Successfully"}, accepted


def addAnswer(token, qid, answerBody):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"message": "Could Not Post Question"}, unAuthorized
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
        return {
            "message": "Answer Posted Successfully",
            "ID": newAnswer.id
            }, accepted


def makeComment(token, qid, commentBody):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"message": "Could Not Post Question"}, unAuthorized
    else:
        newComment = Comment(
            commentUID=tokenValidator[0],
            commentBody=commentBody
            )
        newQuery = Query.objects.get(id=qid)
        newQuery.update(add_to_set__commentList=[newComment])
        return {"message": "Comment Posted Successfully"}, accepted


def displayAllQueries(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"message": "Could Not Post Question"}, unAuthorized
    else:
        return {"message": json.loads(Query.objects.to_json())}, accepted


def displayOneQuery(token, qid):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"message": "Could Not Post Question"}, unAuthorized
    else:
        newQuery = Query.objects.get(id=qid)
        newQuery = json.loads(newQuery.to_json())
        ansList = newQuery['answerList']
        ansListNew = []
        for i in ansList:
            newAns = Answer.objects.get(id=list(i.values())[0])
            ansListNew.append(json.loads(newAns.to_json()))
        newAns['answerList'] = ansListNew
        return {"message": newAns}, accepted


def upvoteAnswer(token, aid):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return {"message": "Could Not Post Question"}, unAuthorized
    else:
        newAnswer = Answer.objects.get(id=aid)
        newAnswer.update(set__answerUpvotes=newAnswer.answerUpvotes+1)
        return {"message": "Answer Upvoted Successfully"}, accepted


def validateToken(token):
    try:
        username = jwt.decode(token, secretKey)["user"]
        try:
            cust = Customers.objects.get(userName=username)
            return cust.userName, True
        except:
            return None, False
    except:
        return None, False
