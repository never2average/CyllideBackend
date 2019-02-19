from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, request
from forumConnectors import addQuery, editQuery, upvoteQuery, addAnswer
from forumConnectors import makeComment, displayAllQueries, displayOneQuery
from forumConnectors import upvoteAnswer
from adminConnectors import adminLogin, getUserCount, getQuizHistory, addQuiz
from adminConnectors import addContest, getContestHistory, getContentAnalysis
from adminConnectors import addContent
from newsConnectors import newsData
from portfolioConnectors import storePortfolios, listMyPortfolios
from portfolioConnectors import listSpecificPortfolios
from confirmationSender import send_confirmation_code
from contentConnectors import viewStories

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


class StorePortfolio(Resource):
    def post(self):
        token = request.headers.get("token")
        data = request.form.get("data")
        resp = make_response(storePortfolios(token, data))
        resp.mimetype = "application/javascript"
        return resp


class DisplayAllPortfolio(Resource):
    def get(self):
        token = request.headers.get("token")
        resp = make_response(listMyPortfolios(token))
        resp.mimetype = "application/javascript"
        return resp


class DisplayOnePortfolio(Resource):
    def get(self):
        token = request.headers.get("token")
        data = request.headers.get("data")
        resp = make_response(listSpecificPortfolios(token, data))
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
        heading = request.form.get("articleHeading")
        author = request.form.get("articleAuthor")
        title = request.form.get("articleTitle")
        picURL = request.form.get("articlePicURL")
        articleURL = request.form.get("articleMDURL")
        contentCreator = addContent(
            token, heading, author, title, picURL, articleURL
            )
        resp = make_response(jsonify(contentCreator[0]), contentCreator[1])
        resp.mimetype = "application/javascript"
        return resp


class AddQuery(Resource):
    def post(self):
        token = request.headers.get("token")
        tags = request.form.get("tags")
        queryBody = request.form.get("qbody")
        queryAdder = addQuery(token, queryBody, tags)
        resp = make_response(
            jsonify(queryAdder[0]),
            queryAdder[1]
        )
        resp.mimetype = "application/javascript"
        return resp


class VerifyPhone(Resource):
    def post(self):
        phone = request.form.get("phone")
        username = request.form.get("username")
        send_confirmation_code(phone)


class EditQuery(Resource):
    def post(self):
        token = request.headers.get("token")
        qid = request.form.get("qid")
        newQueryBody = request.form.get("nquery")
        newQueryTags = request.form.get("tags")
        queryEditor = editQuery(token, qid, newQueryBody, newQueryTags)
        resp = make_response(
            jsonify(queryEditor[0]),
            queryEditor[1]
        )
        resp.mimetype = "application/javascript"
        return resp


class UpvoteQuery(Resource):
    def get(self):
        token = request.headers.get("token")
        qid = request.headers.get("qid")
        queryUpvoter = upvoteQuery(token, qid)
        resp = make_response(jsonify(queryUpvoter[0]), queryUpvoter[1])
        resp.mimetype = "application/javascript"
        return resp


class AddAnswer(Resource):
    def post(self):
        token = request.headers.get("token")
        qid = request.form.get("qid")
        answerBody = request.form.get("answer")
        answerer = makeComment(token, qid, answerBody)
        resp = make_response(
            jsonify(answerer[0]),
            answerer[1]
        )
        resp.mimetype = "application/javascript"
        return resp


class MakeComment(Resource):
    def post(self):
        token = request.headers.get("token")
        qid = request.form.get("qid")
        commentBody = request.form.get("comment")
        commentMaker = makeComment(token, qid, commentBody)
        resp = make_response(
            jsonify(commentMaker[0]),
            commentMaker[1]
        )
        resp.mimetype = "application/javascript"
        return resp


class DisplayAllQueries(Resource):
    def get(self):
        token = request.headers.get("token")
        multiQueryDisplayer = displayAllQueries(token)
        resp = make_response(
            jsonify(multiQueryDisplayer[0]),
            multiQueryDisplayer[1]
            )
        resp.mimetype = "application/javascript"
        return resp


class DisplayOneQuery(Resource):
    def get(self):
        token = request.headers.get("token")
        qid = request.headers.get("qid")
        singleQueryDisplayer = displayOneQuery(token, qid)
        resp = make_response(
            jsonify(singleQueryDisplayer[0]),
            singleQueryDisplayer[1]
            )
        resp.mimetype = "application/javascript"
        return resp


class UpvoteAnswer(Resource):
    def get(self):
        token = request.headers.get("token")
        aid = request.headers.get("aid")
        answerUpvoter = upvoteAnswer(token, aid)
        resp = make_response(jsonify(answerUpvoter[0]), answerUpvoter[1])
        resp.mimetype = "application/javascript"
        return resp


class NewsData(Resource):
    def post(self):
        token = request.headers.get("token")
        articleURL = request.headers.get("articleURL")
        newsRetriever = newsData(token, articleURL)
        resp = make_response(jsonify(newsRetriever[0]), newsRetriever[1])
        resp.mimetype = "application/javascript"
        return resp

api.add_resource(StorePortfolio, "/portfolio/store")
api.add_resource(DisplayAllPortfolio, "/portfolio/display/all")
api.add_resource(DisplayOnePortfolio, "/portfolio/display/one")
api.add_resource(TestConnection, "/testconn")
api.add_resource(AddQuery, '/api/query/add')
api.add_resource(EditQuery, '/api/query/update')
api.add_resource(UpvoteQuery, '/api/query/upvote')
api.add_resource(AddAnswer, '/api/answer/add')
api.add_resource(MakeComment, '/api/comment/add')
api.add_resource(UpvoteAnswer, '/api/answer/upvote')
api.add_resource(DisplayAllQueries, '/api/query/display')
api.add_resource(DisplayOneQuery, '/api/query/display/one')
api.add_resource(AdminLogin, "/admin/login")
api.add_resource(GetUsers, "/api/usercount")
api.add_resource(QuizHistoryAPI, "/api/quiz/history")
api.add_resource(QuizCreationAPI, "/api/quiz/create")
api.add_resource(ContestHistoryAPI, "/api/contest/history")
api.add_resource(ContestCreationAPI, "/api/contest/create")
api.add_resource(ContentAnalysisAPI, "/api/content/analyze")
api.add_resource(ContentAdditionAPI, "/api/content/append")
api.add_resource(VerifyPhone, "/verifyphone")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
