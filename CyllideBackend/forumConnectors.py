from models import Customers, Query, Answer, Comment
from keys import secret_key, data_encryption_key
from simplecrypt import encrypt, decrypt
from statuscodes import unAuthorized, accepted
from datetime import datetime
import json
import jwt
import mongoengine
mongoengine.connect('Cyllide')


def addQuery(token, body, tags):
    tokenValidator = validateToken(token)
    if tokenValidator[1]:
        return json.dumps({"message": "Could Not Post Question"})
    else:
        newQuery = Query(
            queryUID=tokenValidator[0],
            queryBody=body,
            queryTags=tags
            )
        newQuery.save()
        return json.dumps({
            "message": "Question Posted Successfully",
            "ID": json.loads(newQuery.to_json())["_id"]
            }), accepted


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


def upvoteQuery(token, qid):
    tokenValidator = validateToken(token)
    if tokenValidator[1]:
        return json.dumps(
            {"message": "Could Not Post Question"}
            ), unAuthorized
    else:
        newQuery = Query.objects.get(id=qid["$oid"])
        newQuery.update(set__queryUpvotes=newQuery.queryUpvotes+1)
        return json.dumps(
            {"message": "Question Upvoted Successfully"}
        ), accepted


def addAnswer(token, data):
    tokenValidator = validateToken(token)
    if tokenValidator[1]:
        return json.dumps(
            {"message": "Could Not Post Question"}
        ), unAuthorized
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
        return json.dumps({
            "message": "Answer Posted Successfully",
            "ID": newAnswer.id
            }), accepted


def makeComment(token, data):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"message": "Could Not Post Question"}
        ), unAuthorized

    else:
        data = decrypt(data_encryption_key, data).decode('utf-8')
        newComment = Comment(
            commentUID=tokenValidator[0],
            commentBody=data["commentBody"]
            )
        newQuery = Query.objects.get(id=data["qid"])
        newQuery.update(add_to_set__commentList=[newComment])
        return json.dumps(
            {"message": "Comment Posted Successfully"}
        ), accepted


def displayAllQueries(token):
    tokenValidator = validateToken(token)
    if tokenValidator[1]:
        return json.dumps(
            {"message": "Could Not Post Question"}
        ), unAuthorized
    else:
        return json.dumps(
            {
                "message": json.loads(
                    Query.objects().only(
                        "id",
                        "queryBody",
                        "queryTags",
                        "queryLastUpdateTime",
                        "queryNumViews"
                        ).to_json()
                    )
            }
        ), accepted


def displayOneQuery(token, qid):
    tokenValidator = validateToken(token)
    if tokenValidator[1]:
        return json.dumps({"message": "Could Not Post Question"}), unAuthorized
    else:
        newQuery = Query.objects.get(id=qid['$oid'])
        newQuery.update(inc__queryNumViews = 1)
        newQuery = json.loads(newQuery.to_json())
        ansList = newQuery['answerList']
        ansListNew = []
        for i in ansList:
            newAns = Answer.objects.get(id=ansList(i.values())[0])
            ansListNew.append(json.loads(newAns.to_json()))
        newQuery['answerList'] = ansListNew
        return json.dumps({"message": newQuery}), accepted


def upvoteAnswer(token, aid):
    tokenValidator = validateToken(token)
    if tokenValidator[1]:
        return json.dumps(
            {"message": "Could Not Post Question"}
        ), unAuthorized
    else:
        newAnswer = Answer.objects.get(id=aid)
        newAnswer.update(set__answerUpvotes=newAnswer.answerUpvotes+1)
        return json.dumps(
            {"message": "Answer Upvoted Successfully"}
        ), accepted


def validateToken(token):
    try:
        username = jwt.decode(token, secret_key)["user"]
        try:
            cust = Customers.objects.get(userName=username)
            return cust.userName, True
        except Exception:
            return "None", False
    except Exception:
        return "None", False

# TODO Phone Authentication required

if __name__ == "__main__":
    # print(addQuery("wdjchnsx","How do stock markets work?", ["Business", "Finance"]))
    # print(addQuery("wdjchnsx","How do stock markets work?", ["Business", "Finance"]))
    # print(displayAllQueries("ehfvkdbwcmklx"))
    print(displayOneQuery("ehfvkdbwcmklx", {"$oid": "5c8fe266b85f286f5f44c890"}))
