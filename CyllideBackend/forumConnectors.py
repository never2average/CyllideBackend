from models import Customers, Query, Answer, Comment
from keys import secret_key
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
            queryTags=json.loads(tags)
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
        newQuery = Query.objects.get(id=qid)
        newQuery.update(set__queryBody=queryBodyNew)
        newQuery.update(set__queryLastUpdateTime=datetime.now())
        newQuery.update(set__queryTags=json.loads(queryTagsNew))
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
        cust = Customers.objects.get(userName=tokenValidator[0])
        cust.update(inc__questionsAnswered=1)
        newAnswer = Answer(
            answerUID=tokenValidator[0],
            answerBody=answerBody,
            profilePic=cust.profilePic
            )
        newAnswer.save()
        newQuery = Query.objects.get(id=qid)
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
        newQuery = Query.objects.get(id=qid)
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
        newQuery = Query.objects.get(id=qid)
        newQuery.update(inc__queryNumViews=1)
        newQuery = json.loads(newQuery.to_json())
        ansList = newQuery['answerList']
        print(ansList)
        ansListNew = []
        for i in ansList:
            newAns = Answer.objects.get(id=i["$oid"])
            newAns = json.loads(newAns.to_json())
            if newAns["profilePic"] == "https://www.freeiconspng.com/uploads/profile-icon-9.png":
                newAns["profilePic"] = "https://firebasestorage.googleapis.com/v0/b/cyllide.appspot.com/o/defaultuser.png?alt=media&token=0453d4ba-82e8-4b6c-8415-2c3761d8b345"
            ansListNew.append()
        newQuery['answerList'] = ansListNew
        # default=
        return json.dumps({"message": newQuery}), accepted


# Checked: Working
def upvoteAnswer(token, aid, isTrue):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"message": "Could Not Post Question"}
        ), unAuthorized
    else:
        newAnswer = Answer.objects.get(id=aid)
        if isTrue == "1":
            newAnswer.update(set__answerUpvotes=newAnswer.answerUpvotes+1)
            return json.dumps(
                {
                    "message": "Answer Upvoted Successfully",
                    "numUpvotes": str(newAnswer.answerUpvotes+1)
                }
            ), accepted
        elif isTrue == "-1":
            newAnswer.update(set__answerUpvotes=newAnswer.answerUpvotes-1)
            return json.dumps(
                {
                    "message": "Answer Upvoted Successfully",
                    "numUpvotes": str(newAnswer.answerUpvotes-1)
                }
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
# print(addQuery("wdjchnsx","How do stock markets work?", json.dumps([])))
# print(addAnswer("efhvkcnwldx","5c92b267b85f282163e50fab","My answer1"))
# print(displayOneQuery("ehfvkdbwcmklx", "5c92b267b85f282163e50fab"))
# print(makeComment("efhvkcnwldx",{"$oid": "5c8ff890b85f280607875af2"},
# "My comment1"))
# print(json.loads(displayAllQueries("ehfvkdbwcmklx")[0])["message"][0])
# print(upvoteAnswer("jhwbdcxqs",{"$oid": "5c8ffa79b85f280780f2041e"}))
# print(editQuery("jhwbdcxqs", {"$oid": "5c8ff890b85f280607875af2"},
#  "I changed my question", ["Business"]))
