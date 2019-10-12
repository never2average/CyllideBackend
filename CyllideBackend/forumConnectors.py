from models import Customers, Query, Answer, Comment
from models import Notifications
from keys import secret_key
from statuscodes import unAuthorized, accepted
from datetime import datetime
import json
import jwt


# Checked: Working
def addQuery(token, body, tags):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"message": "Could Not Post Question"}), unAuthorized
    else:
        newQuery = Query(
            queryUID=tokenValidator[0],
            queryBody=body,
            queryTags=json.loads(tags),
            queryTime=datetime.now(),
            queryLastUpdateTime=datetime.now()
        )
        newQuery.save()
        Customers.objects(userName=tokenValidator[0]).update(
            inc__cyllidePoints=40
        )
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
        newQuery.update(
            set__queryBody=queryBodyNew,
            set__queryLastUpdateTime=datetime.now(),
            set__queryTags=json.loads(queryTagsNew)
        )
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
        cust.update(
            inc__questionsAnswered=1,
            inc__cyllidePoints=40
        )
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
        ansListNew = []
        ansUIDs = []
        for i in ansList:
            try:
                newAns = Answer.objects.get(id=i["$oid"])
                newAns = json.loads(newAns.to_json())
                ansListNew.append(newAns)
                ansUIDs.append(newAns["answerUID"])
            except:
                return json.dumps({"message": i}), accepted
        ansUIDs = list(set(ansUIDs))
        if tokenValidator[0] in ansUIDs:
            ansUIDs.remove(tokenValidator[0])
        Customers.objects(userName__in=ansUIDs).update(
            inc__cyllidePoints=1
        )
        newQuery['answerList'] = ansListNew
        return json.dumps({"message": newQuery}), accepted


# Checked: Working
def upvoteAnswer(token, aid, isTrue):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"message": "Could Not Post Question"}), unAuthorized
    else:
        newAnswer = Answer.objects.get(id=aid)
        if tokenValidator[0] not in newAnswer.answerUpvoters:
            if isTrue == "1":
                newAnswer.update(set__answerUpvotes=newAnswer.answerUpvotes+1)
                newAnswer.update(
                    add_to_set__answerUpvoters=[tokenValidator[0]]
                    )
                Customers.objects(userName=newAnswer.answerUID).update(
                    inc__cyllidePoints=4
                )
                notification = Notifications(
                    username=newAnswer.answerUID,
                    message=tokenValidator[0]+" upvoted your answer",
                    notificationTime=datetime.now()
                    )
                notification.save()
                return json.dumps({
                    "message": "Answer Upvoted Successfully",
                    "numUpvotes": str(newAnswer.answerUpvotes+1)
                }), accepted
            elif isTrue == "-1":
                newAnswer.update(set__answerUpvotes=newAnswer.answerUpvotes-1)
                newAnswer.update(
                    add_to_set__answerUpvoters=[tokenValidator[0]]
                )
                return json.dumps({
                    "message": "Answer Upvoted Successfully",
                    "numUpvotes": str(newAnswer.answerUpvotes-1)
                }), accepted
        else:
            return json.dumps({
                "message": "Answer Upvoted Successfully",
                "numUpvotes": str(newAnswer.answerUpvotes)
            }), accepted


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


if __name__ == "__main__":
    import mongoengine
    from keys import username_db, password_db
    mongoengine.connect(
        db='Cyllide',
        username=username_db,
        password=password_db,
        authentication_source='Cyllide'
    )
    questions = [
        "What is market cap of a company?",
        "Is a stock bought on the basis of the company's profits?",
        "Why important companies like Amazon are not included in Dow Jones index?",
        "Why do rich people invest in hedge funds if, in the long term, index funds beat them?"
    ]
    answers = [
        "Market cap is the price of a share multiplied by no of outstanding shares. In a hypothethical situation if you want to buy a company this is the price you pay. Outstanding shares include shares present with the promoter and shares that traded on the stock exchange.",
        "Tesla has had a loss of nearly $2 Billion in 2017 but from the time it got listed on the stock exchange in 2010 it boasts a staggering 1500% of returns. Investors saw future value in this stock. Only some conventional stocks are priced according to their profits. Similarly, Amazon has it's majority of revenue from cloud which is operationally profitable and this number is only increasing. So investors see a lot of future growth in this spectrum whose addressable market is only increasing.",
        "Because it is a price-weighted index which means if a stock with very high price is included then it can skew the whole index towards it's returns. Take Berkshire Hathaway's (NYSE: BRK.A) stock for example which trades at nearly $315k as of today. If it's included in DJIA with it's present constituent stocks then It's weightage will be a staggering 99% which doesn't make sense. So it'll never be included. This makes DJIA naturally flawed. Other indices work on 'market-cap weighted' or'free-float market cap weighted'. Indian Indices are calculated based on the latter.",
        "Yeah it's true that majority of hedge funds don't beat the market because they have a greater purpose than to beat the market i.e they are meant to preserve their investor's money irrespective of the market volatality. That's the reaseon they are preferred by rich investors."
    ]
    tags = [
        ["Finance", "Stock Markets"],
        ["Finance", "Stock Markets", "Macro-Economics"],
        ["Finance", "Stock Markets"],
        ["Finance", "Macro-Economics"]
    ]
    n = len(questions)
    for i in range(n):
        answer = Answer(
            answerUID="Priyesh",
            answerBody=answers[i]
        )
        answer.save()
        question = Query(
            queryUID="Prasann",
            queryBody=questions[i],
            answerList=[answer.id],
            queryTags=tags[i],
            queryTime=datetime.now()
        )
        question.save()
