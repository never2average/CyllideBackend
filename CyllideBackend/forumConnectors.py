from models import Customers, Query, Answer, Comment
from keys import secret_key, data_encryption_key
from simplecrypt import encrypt, decrypt
from statuscodes import unAuthorized, accepted
from datetime import datetime
import json
import jwt
import mongoengine
mongoengine.connect('Cyllide')


# Checked: Working
def addQuery(token, body, tags):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
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


# Checked: working
def editQuery(token, qid, queryBodyNew, queryTagsNew):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"message": "Could Not Post Question"}
            ), unAuthorized
    else:
        newQuery = Query.objects.get(id=qid["$oid"])
        newQuery.update(set__queryBody=queryBodyNew)
        newQuery.update(set__queryLastUpdateTime=datetime.now())
        newQuery.update(set__queryTags=queryTagsNew)
        return json.dumps(
            {"message": "Question Edited Successfully"}
            ), accepted


# Checked: working
def addAnswer(token, qid, answerBody):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"message": "Could Not Post Question"}
        ), unAuthorized
    else:
        newAnswer = Answer(
            answerUID=tokenValidator[0],
            answerBody=answerBody
            )
        newAnswer.save()
        newQuery = Query.objects.get(id=qid["$oid"])
        newQuery.update(add_to_set__answerList=[newAnswer.id])
        newQuery.update(set__isAnswered=True)
        return json.dumps({
            "message": "Answer Posted Successfully",
            "ID": json.loads(newAnswer.to_json())["_id"]
            }), accepted


# Checked: Working
def makeComment(token, qid, commentBody):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"message": "Could Not Post Question"}
        ), unAuthorized

    else:
        newComment = Comment(
            commentUID=tokenValidator[0],
            commentBody=commentBody
            )
        newQuery = Query.objects.get(id=qid["$oid"])
        newQuery.update(add_to_set__commentList=[newComment])
        return json.dumps(
            {"message": "Comment Posted Successfully"}
        ), accepted


# Checked: Working
def displayAllQueries(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
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


# Checked: Working
def displayOneQuery(token, qid):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
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


# Checked: Working
def upvoteAnswer(token, aid):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"message": "Could Not Post Question"}
        ), unAuthorized
    else:
        newAnswer = Answer.objects.get(id=aid["$oid"])
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

# if __name__ == "__main__":
    # print(addQuery("wdjchnsx","How do stock markets work?", ["Business", "Finance"]))
    # print(addQuery("wdjchnsx","How do stock markets work?", ["Business", "Finance"]))
    # print(displayAllQueries("ehfvkdbwcmklx"))
    # print(displayOneQuery("ehfvkdbwcmklx", {"$oid": "5c8ff890b85f280607875af2"}))
    # print(makeComment("efhvkcnwldx",{"$oid": "5c8ff890b85f280607875af2"},"My comment1"))
    # print(addAnswer("efhvkcnwldx",{"$oid": "5c8ff890b85f280607875af2"},"My answer1"))
    # print(upvoteAnswer("jhwbdcxqs",{"$oid": "5c8ffa79b85f280780f2041e"}))
    # print(editQuery("jhwbdcxqs", {"$oid": "5c8ff890b85f280607875af2"}, "I changed my question", ["Business"]))
