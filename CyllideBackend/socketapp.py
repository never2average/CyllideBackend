from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_restful import Api, Resource
from models import Quiz, Questions
import json
import mongoengine
from datetime import datetime
mongoengine.connect("Cyllide")


app = Flask(__name__)
socketio = SocketIO(app)
api = Api(app)


@socketio.on("message")
def handleMessage(message={"qid": "5cd43bccb85f2824ac4887b7"}):
    qid = message["qid"]
    questionList = json.loads(
        Quiz.objects(id=qid, quizStartTime__gte=datetime.now()).to_json()
        )[0]["quizQuestions"]
    questions = []
    for i in questionList:
        questions.append(
            json.loads(Questions.objects.get(id=i["$oid"]).to_json())
            )
    questions.sort(key=lambda x: x["appearancePosition"])
    for i in range(10):
        question = questions[i]
        data = {
            "id": question["_id"]["$oid"],
            "question": question["theQuestion"],
            "options": [j["value"] for j in question["answerOptions"]]
            }
        send(data, broadcast=True)
        socketio.sleep(1)


@socketio.on("response")
def handleResponse(responseData):
    question = Questions.objects.get(id=responseData["id"])
    answerList = question.answerOptions
    value = "Wrong"
    for i in answerList:
        if i.value == responseData["option"]:
            if i.isCorrect != 0:
                to_inc = dict(
                    inc__answerOptions__S__numResponses=1,
                    inc__numResponses=1,
                    inc__numSuccessfulResponses=1
                    )
                Questions.objects(
                    id=responseData["id"],
                    answerOptions__value=i.value
                    ).update(**to_inc)
                value = "Correct"
            else:
                to_inc = dict(
                    inc__answerOptions__S__numResponses=1,
                    inc__numResponses=1
                    )
                Questions.objects(
                    id=responseData["id"],
                    answerOptions__value=i.value
                    ).update(**to_inc)
            break
    question = json.loads(
        Questions.objects.get(id=responseData["id"]).to_json()
        )
    emit(
        "amicorrect",
        {
            "myresp": value
        }
    )
    if question["appearancePosition"] == 1:
        if question["numResponses"] >= len(Quiz.objects.get(id=responseData["qid"]).quizParticipants):
            emit(
                "response_results",
                {
                    "question": question["theQuestion"],
                    "totalresponses": question["numResponses"],
                    "optionsData": question["answerOptions"]
                },
                broadcast=True
            )

    else:
        totalResp = 0
        questions = Quiz.objects.get(id=responseData["qid"]).quizQuestions
        for i in questions:
            try:
                quest = Questions.objects.get(id=i)
            except Exception:
                quest = i
            if quest.appearancePosition == question["appearancePosition"] - 1:
                totalResp = quest.numSuccessfulResponses
                break
        if question["numResponses"] >= totalResp:
            emit(
                "response_results",
                {
                    "question": question["theQuestion"],
                    "totalresponses": question["numResponses"],
                    "optionsData": question["answerOptions"]
                },
                broadcast=True
            )


class SomeApi(Resource):
    def get(self):
        return "api works simultaneously"


api.add_resource(SomeApi, "/api")


if __name__ == "__main__":
    socketio.run(app, debug=True)
