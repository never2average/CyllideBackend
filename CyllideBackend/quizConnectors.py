from models import Quiz, Questions, Customers, Award
import json
from keys import secret_key
import jwt
from statuscodes import unAuthorized, working, limitExceeded
from datetime import datetime


def displayCount(token, questionID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        questionData = json.loads(Questions.objects.get(
            id=questionID).to_json())
        return json.dumps({"data": questionData["numResponses"]}), working


def submitAnswer(token, questionID, optionValue):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        questionData = Questions.objects.get(id=questionID)
        answerList = questionData.answerOptions
        for i in answerList:
            if i.value == optionValue:
                if i.isCorrect != 0:
                    to_inc = dict(inc__answerOptions__S__numResponses=1, inc__numResponses=1, inc__numSuccessfulResponses=1)
                    Questions.objects(id=questionID, answerOptions__value=i.value).update(**to_inc)
                    return json.dumps({"data": "Correct"}), working
                else:
                    to_inc = dict(inc__answerOptions__S__numResponses=1, inc__numResponses=1)
                    Questions.objects(id=questionID, answerOptions__value=i.value).update(**to_inc)
                    return json.dumps({"data": "Wrong"}), working
        to_inc = dict(inc__answerOptions__S__numResponses=1, inc__numResponses=1)
        Questions.objects(id=questionID, answerOptions__value=i.value).update(**to_inc)
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
        return json.dumps({"data": questionList}), working


def quizStats(token, questionID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps({"data": "Need to login first"}), unAuthorized
    else:
        quest = Questions.objects(id=questionID).only("id","answerOptions").to_json()
        return json.dumps({"data":json.loads(quest)}), working


def reviveQuiz(token, numCoins, questionID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        to_inc = dict(inc__numResponses=1, inc__numSuccessfulResponses=1)
        Questions.objects(id=questionID).update(**to_inc)
        Customers.objects(userName=tokenValidator[0]).update(set__numCoins=numCoins)
        return json.dumps(
            {"data": "Coins Updated"}
        ), working


def getLatestQuiz(token):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        latestQuiz = Quiz.objects(quizStartTime__gte=datetime.now()).order_by('quizStartTime').exclude('quizQuestions', "quizWinners", "quizParticipants").first().to_json()
        if latestQuiz is not None:
            return json.dumps({"data": json.loads(latestQuiz)}), working
        else:
            return json.dumps({"data": ""}), working


def numProceeders(token, questionID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        return json.dumps(
            {"data": json.loads(Questions.objects(id=questionID).only("id", "numSuccessfulResponses").to_json())}
        ), working


def quizRewards(token, quizID, upiID):
    tokenValidator = validateToken(token)
    if not tokenValidator[1]:
        return json.dumps(
            {"data": "Need to login first"}
        ), unAuthorized
    else:
        try:
            cust = Customers.objects.get(userName=username)
            cust.update(inc__quizzesWon=1)
            quiz = Quiz.objects.get(id=quizID)
            aw = Award(quizID=quiz.id,username=tokenValidator[0],UPI=upiID)
            aw.save()
        except Exception:
            return json.dumps({"data": "InvalidQuizID"}), unAuthorized


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
        "prasannkumar1263"
        )[0]["token"]

    for i in range(23):
        quizData = {
            "start_date": "Apr 14 2019 {}:{}",
            "questions":
            [
                {
                    "question": "Who was the founder of 'Reliance Industries'?",
                    "options": {
                        "Mukesh Ambani": 0,
                        "Anil Ambani": 0,
                        "Nita Ambani": 0,
                        "Dhirubai Ambani": 1
                        }
                },
                {
                    "question": "Who is the current finance minister of India?",
                    "options": {
                        "Manmohan Singh": 0,
                        "P.Chidambaram": 0,
                        "Arun Jaitley": 1,
                        "Sheila Dixit ": 0
                        }
                },
                {
                    "question": "Which publically traded company has the highest market revenue?",
                    "options": {
                        "SAUDI ARAMCO": 0,
                        "APPLE": 0,
                        "AMAZON": 0,
                        "WALMART": 1
                        }
                },
                {
                    "question": "How many times does the monetary policy committee meet?",
                    "options": {
                        "4": 0,
                        "12": 0,
                        "8": 1,
                        "6": 0
                        }
                },
                {
                    "question": "What is the full form of GDP?",
                    "options": {
                        "Gross Domestic Product": 1,
                        "Gross Domestic Price": 0,
                        "General Domestic Price": 0,
                        "General Domestic Product": 0
                        }
                },
                {
                    "question": "What do you mean by 'bull market' in stock market terminology?",
                    "options": {
                        "Markets hitting highs": 1,
                        "Markets hitting lows": 0,
                        "Markets deviating much": 1,
                        "None of the above ": 0
                    }
                },
                {
                    "question": "What do you mean by 'bull market' in stock market terminology?",
                    "options": {
                        "Markets hitting highs": 0,
                        "Markets hitting lows": 1,
                        "Markets not deviating much": 0,
                        "None of the above": 0
                    }
                },
                {
                    "question": "What percent of Indian population invest in stock markets?",
                    "options": {
                        "10 %": 0,
                        "20 %": 0,
                        "30 %": 0,
                        "2 %": 1
                    }
                },
                {
                    "question": "Which of the company does Elon Musk not own at any point of time?",
                    "options": {
                        "Paypal": 0,
                        "General Motors": 1,
                        "SpaceX": 0,
                        "Tesla": 0
                    }
                },
                {
                    "question": "Which company did Newton invest in that made him huge losses?",
                    "options": {
                        "Genral Motors": 0,
                        "Ford": 0,
                        "South Sea Company": 1,
                        "East India Company": 0
                    }
                }
            ]
        }
        for j in range(0, 60, 5):
            quizData["start_date"] = quizData["start_date"].format(i, j)
            quizData = json.dumps(quizData)
            dummyQuiz = addQuiz(token, quizData)
            print(dummyQuiz)
