from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, request
from adminConnectors import adminLogin, getUserCount, quizHistorian, addQuiz
from adminConnectors import addContest, getContestHistory, getContentAnalysis
from adminConnectors import addContent


app = Flask(__name__)
api = Api(app)


class TestConnection(Resource):
    def get(self):
        return jsonify({
            "message": "APIS working"
            })


class AdminLogin(Resource):
    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        loginProcessor = adminLogin(email, password)
        resp = make_response(jsonify(loginProcessor[0]), loginProcessor[1])
        resp.mimetype = "application/javascript"
        return resp


class GetUsers(Resource):
    def get(self):
        token = request.headers.get("token")
        countProcessor = getUserCount(token)
        resp = make_response(jsonify(countProcessor[0]), countProcessor[1])
        resp.mimetype = "application/javascript"
        return resp


class QuizHistoryAPI(Resource):
    def get(self):
        token = request.headers.get("token")
        quizHistorian = getQuizHistory(token)
        resp = make_response(jsonify(quizHistorian[0]), quizHistorian[1])
        resp.mimetype = "application/javascript"
        return resp


class QuizCreationAPI(Resource):
    def post(self):
        token = request.headers.get("token")
        data = request.form.get("data")
        quizCreator = addQuiz(token, data)
        resp = make_response(jsonify(quizCreator[0]), quizCreator[1])
        resp.mimetype = "application/javascript"
        return resp


class ContestHistoryAPI(Resource):
    def get(self):
        token = request.headers.get("token")
        contestHistorian = getContestHistory(token)
        resp = make_response(jsonify(contestHistorian[0]), contestHistorian[1])
        resp.mimetype = "application/javascript"
        return resp


class ContestCreationAPI(Resource):
    def post(self):
        token = request.headers.get("token")
        data = request.form.get("data")
        contestCreator = addContest(token, data)
        resp = make_response(jsonify(contestCreator[0]), contestCreator[1])
        resp.mimetype = "application/javascript"
        return resp


class ContentAnalysisAPI(Resource):
    def get(self):
        token = request.headers.get("token")
        contentAnalyzer = getContentAnalysis(token)
        resp = make_response(jsonify(contentAnalyzer[0]), contentAnalyzer[1])
        resp.mimetype = "application/javascript"
        return resp


class ContentAdditionAPI(Resource):
    def post(self):
        token = request.headers.get("token")
        data = request.form.get("data")
        contentCreator = addContent(token, data)
        resp = make_response(jsonify(contentCreator[0]), contentCreator[1])
        resp.mimetype = "application/javascript"
        return resp


api.add_resource(TestConnection, "/testconn")
api.add_resource(AdminLogin, "/admin/login")
api.add_resource(GetUsers, "/api/usercount")
api.add_resource(QuizHistoryAPI, "/api/quiz/history")
api.add_resource(QuizCreationAPI, "/api/quiz/create")
api.add_resource(ContestHistoryAPI, "/api/contest/history")
api.add_resource(ContestCreationAPI, "/api/contest/create")
api.add_resource(ContentAnalysisAPI, "/api/content/analyze")
api.add_resource(ContentAdditionAPI, "/api/content/append")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
