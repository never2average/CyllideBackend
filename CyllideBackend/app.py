from flask import Flask, jsonify, make_response, render_template
from flask_restful import Resource, Api, request
from forumConnectors import addQuery, editQuery, upvoteAnswer, addAnswer
from forumConnectors import makeComment, displayAllQueries, displayOneQuery
from adminConnectors import adminLogin, getUserCount, getQuizHistory, addQuiz
from adminConnectors import addContest, getContestHistory, getContentAnalysis
from adminConnectors import addContent
from newsConnectors import newsData
from portfolioConnectors import makePortfolios, listMyPortfolios, listPositions
from portfolioConnectors import takePosition, deletePosition
from confirmationSender import sendOTP, verifyOTP, setPicURL, getPicURL
from confirmationSender import getProfileInfo, getProfileInfoOthers
from confirmationSender import sendFeedback
from contentConnectors import viewStories, updateStories
from quizConnectors import displayCount, submitAnswer, getQuiz, reviveQuiz
from quizConnectors import getLatestQuiz, quizStats, numProceeders, quizRewards
from contestConnectors import enrolPortfolio, getLeaderBoard, listAllContests
from contestConnectors import listRelevantPortfolios

app = Flask(__name__)
api = Api(app)


@app.route("/")
def documentation():
    return render_template("index.html")


class GetLatestQuiz(Resource):
    def get(self):
        token = request.headers.get("token")
        resp = make_response(getLatestQuiz(token))
        resp.mimetype = "application/javascript"
        return resp


class EnrollPortfolio(Resource):
    def post(self):
        token = request.headers.get("token")
        contestUID = request.headers.get("contestUID")
        portfolioUID = request.headers.get("portfolioUID")
        resp = make_response(enrolPortfolio(token, contestUID, portfolioUID))
        resp.mimetype = "application/javascript"
        return resp


class ReviveQuiz(Resource):
    def post(self):
        token = request.headers.get("token")
        numCoins = request.headers.get("coins")
        questionID = request.headers.get("questionID")
        resp = make_response(reviveQuiz(token, numCoins, questionID))
        resp.mimetype = "application/javascript"
        return resp


class GetLeaderBoard(Resource):
    def post(self):
        token = request.headers.get("token")
        data = request.headers.get("contestUID")
        resp = make_response(getLeaderBoard(token, data))
        resp.mimetype = "application/javascript"
        return resp


class ListAllContests(Resource):
    def get(self):
        token = request.headers.get("token")
        capex = request.headers.get("capex")
        resp = make_response(listAllContests(token, capex))
        resp.mimetype = "application/javascript"
        return resp


class GetQuiz(Resource):
    def get(self):
        token = request.headers.get("token")
        data = request.headers.get("quizID")
        resp = make_response(getQuiz(token, data))
        resp.mimetype = "application/javascript"
        return resp


class UpdateStories(Resource):
    def post(self):
        token = request.headers.get("token")
        timeInMins = request.headers.get("timeRead")
        contentID = request.headers.get("contentID")
        resp = make_response(
            updateStories(token, contentID, timeInMins)
        )
        resp.mimetype = "application/javascript"
        return resp


class SubmitResponse(Resource):
    def post(self):
        token = request.headers.get("token")
        questionID = request.headers.get("questionID")
        optionValue = request.headers.get("optionValue")
        resp = make_response(
            submitAnswer(token, questionID, optionValue)
        )
        resp.mimetype = "application/javascript"
        return resp


class DisplayCount(Resource):
    def post(self):
        token = request.headers.get("token")
        questionID = request.headers.get("questionID")
        resp = make_response(
            displayCount(token, questionID)
        )
        resp.mimetype = "application/javascript"
        return resp


class ViewStories(Resource):
    def post(self):
        token = request.headers.get("token")
        resp = make_response(
            viewStories(token)
        )
        resp.mimetype = "application/javascript"
        return resp


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


class MakePortfolio(Resource):
    def post(self):
        token = request.headers.get("token")
        name = request.headers.get("name")
        capex = request.headers.get("capex")
        resp = make_response(makePortfolios(token, name, capex))
        resp.mimetype = "application/javascript"
        return resp


class DisplayAllPortfolio(Resource):
    def get(self):
        token = request.headers.get("token")
        resp = make_response(listMyPortfolios(token))
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
        data = request.get_data()
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
        data = request.get_data()
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
        author = request.form.get("articleAuthor")
        title = request.form.get("articleTitle")
        picURL = request.form.get("articlePicURL")
        articleURL = request.form.get("articleMDURL")
        cType = request.form.get("contentType")
        contentSummary = request.form.get("contentSummary")
        contentCreator = addContent(
            token, author, title, picURL, articleURL, cType, contentSummary
            )
        resp = make_response(jsonify(contentCreator[0]), contentCreator[1])
        resp.mimetype = "application/javascript"
        return resp


class SendOTP(Resource):
    def post(self):
        phone = request.headers.get("phone")
        username = request.headers.get("username")
        otpSender = sendOTP(phone, username)
        resp = make_response(jsonify(otpSender[0]), otpSender[1])
        resp.mimetype = "application/javascript"
        return resp


class AddQuery(Resource):
    def post(self):
        token = request.headers.get("token")
        body = request.headers.get("body")
        tags = request.headers.get("tags")
        resp = make_response(addQuery(token, body, tags))
        resp.mimetype = "application/javascript"
        return resp


class EditQuery(Resource):
    def post(self):
        token = request.headers.get("token")
        qid = request.headers.get("qid")
        queryBody = request.headers.get("queryBody")
        queryTags = request.headers.get("queryHeaders")
        resp = make_response(editQuery(token, qid, queryBody, queryTags))
        resp.mimetype = "application/javascript"
        return resp


class AddAnswer(Resource):
    def post(self):
        token = request.headers.get("token")
        qid = request.headers.get("qid")
        answerBody = request.headers.get("answerBody")
        resp = make_response(
            addAnswer(token, qid, answerBody)
        )
        resp.mimetype = "application/javascript"
        return resp


class MakeComment(Resource):
    def post(self):
        token = request.headers.get("token")
        qid = request.headers.get("qid")
        commentBody = request.headers.get("commentBody")
        resp = make_response(
            makeComment(token, qid, commentBody)
        )
        resp.mimetype = "application/javascript"
        return resp


class DisplayAllQueries(Resource):
    def get(self):
        token = request.headers.get("token")
        resp = make_response(
            displayAllQueries(token)
            )
        resp.mimetype = "application/javascript"
        return resp


class DisplayOneQuery(Resource):
    def get(self):
        token = request.headers.get("token")
        qid = request.headers.get("qid")
        resp = make_response(
            displayOneQuery(token, qid)
            )
        resp.mimetype = "application/javascript"
        return resp


class UpvoteAnswer(Resource):
    def get(self):
        token = request.headers.get("token")
        aid = request.headers.get("aid")
        isTrue = request.headers.get("votes")
        resp = make_response(upvoteAnswer(token, aid, isTrue))
        resp.mimetype = "application/javascript"
        return resp


class NewsData(Resource):
    def post(self):
        token = request.headers.get("token")
        url = request.headers.get("url")
        resp = make_response(newsData(token, url))
        resp.mimetype = "application/javascript"
        return resp


class VerifyOTP(Resource):
    def post(self):
        phone = request.headers.get("phone")
        otp = request.headers.get("otp")
        referee = request.headers.get("referee")
        otpValidator = verifyOTP(phone, otp, referee)
        resp = make_response(jsonify(otpValidator[0]), otpValidator[1])
        resp.mimetype = "application/javascript"
        return resp


class ListRelevantPortfolios(Resource):
    def get(self):
        token = request.headers.get("token")
        capex = request.headers.get("capex")
        relevantLister = listRelevantPortfolios(token, capex)
        resp = make_response(jsonify(relevantLister[0]), relevantLister[1])
        resp.mimetype = "application/javascript"
        return resp


class ListPositions(Resource):
    def get(self):
        token = request.headers.get("token")
        portfolioID = request.headers.get("portfolioID")
        posType = request.headers.get("posType")
        return make_response(listPositions(token,portfolioID, posType))


class TakePosition(Resource):
    def post(self):
        token = request.headers.get("token")
        portfolioID = request.headers.get("portfolioID")
        ticker = request.headers.get("ticker")
        quantity = request.headers.get("quantity")
        isLong = request.headers.get("isLong")
        return make_response(takePosition(token, portfolioID, ticker, quantity, isLong))

    def delete(self):
        token = request.headers.get("token")
        portfolioID = request.headers.get("portfolioID")
        state = request.headers.get("state")
        ticker = request.headers.get("ticker")
        entryTime = request.headers.get("entryTime")
        return make_response(deletePosition(token, portfolioID, state, ticker, entryTime))



class QuestionStats(Resource):
    def get(self):
        token = request.headers.get("token")
        questionID = request.headers.get("questionID")
        return make_response(quizStats(token, questionID))


class NumProceeders(Resource):
    def get(self):
        token = request.headers.get("token")
        questionID = request.headers.get("questionID")
        return make_response(numProceeders(token, questionID))


class ProfilePic(Resource):
    def get(self):
        token = request.headers.get("token")
        return make_response(getPicURL(token))

    def put(self):
        token = request.headers.get("token")
        profilePic = request.headers.get("profileURL")
        return make_response(setPicURL(token, profilePic))


class ProfileInfo(Resource):
    def get(self):
        token = request.headers.get("token")
        username = request.headers.get("username")
        if username != None:
            return make_response(getProfileInfoOthers(token, username))    
        return make_response(getProfileInfo(token))


class SendFeedback(Resource):
    def post(self):
        token = request.headers.get("token")
        text = request.headers.get("text")
        return make_response(sendFeedback(token,text))


class QuizReward(Resource):
    def post(self):
        token = request.headers.get("token")
        quizID = request.headers.get("quizID")
        upiID = request.headers.get("upiID")
        return make_response(quizRewards(token, quizID, upiID))


# All the client APIs
api.add_resource(QuizReward, "/api/client/quiz/reward")
api.add_resource(SendFeedback, "/api/client/sendfeedback")
api.add_resource(ProfileInfo, "/api/client/profileinfo")
api.add_resource(ProfilePic, "/api/client/profilepic")
api.add_resource(NumProceeders, "/api/client/quiz/nextques")
api.add_resource(QuestionStats, "/api/client/quiz/stats")
api.add_resource(TakePosition, "/api/client/portfolio/order")
api.add_resource(SendOTP, "/api/client/auth/otp/send")
api.add_resource(VerifyOTP, "/api/client/auth/otp/verify")
api.add_resource(SubmitResponse, "/api/client/quiz/submit")
api.add_resource(DisplayCount, "/api/client/quiz/getcount")
api.add_resource(GetQuiz, "/api/client/quiz/get")
api.add_resource(GetLatestQuiz, "/api/client/quiz/get/latest")
api.add_resource(ReviveQuiz, '/api/client/quiz/revive')
api.add_resource(ViewStories, "/api/client/stories/view")
api.add_resource(UpdateStories, '/api/client/stories/update')
api.add_resource(MakePortfolio, "/api/client/portfolio/create")
api.add_resource(DisplayAllPortfolio, "/api/client/portfolio/display/all")
api.add_resource(ListPositions, "/api/client/portfolios/positionlist")
api.add_resource(AddQuery, '/api/client/query/add')
api.add_resource(AddAnswer, '/api/client/answer/add')
api.add_resource(MakeComment, '/api/client/comment/add')
api.add_resource(EditQuery, '/api/client/query/update')
api.add_resource(UpvoteAnswer, '/api/client/answer/upvote')
api.add_resource(DisplayAllQueries, '/api/client/query/display')
api.add_resource(DisplayOneQuery, '/api/client/query/display/one')
api.add_resource(EnrollPortfolio, '/api/client/contest/enroll/portfolio')
api.add_resource(ListAllContests, '/api/client/contest/list')
api.add_resource(ListRelevantPortfolios, '/api/client/contest/list/portfolios/rel')
api.add_resource(GetLeaderBoard, '/api/client/contest/leaderboard')
api.add_resource(NewsData, "/api/news/get")


# All the admin APIs
api.add_resource(AdminLogin, "/api/admin/login")
api.add_resource(GetUsers, "/api/admin/usercount")
api.add_resource(QuizHistoryAPI, "/api/admin/quiz/history")
api.add_resource(QuizCreationAPI, "/api/admin/quiz/create")
api.add_resource(ContestHistoryAPI, "/api/admin/contest/history")
api.add_resource(ContestCreationAPI, "/api/admin/contest/create")
api.add_resource(ContentAnalysisAPI, "/api/admin/content/analyze")
api.add_resource(ContentAdditionAPI, "/api/admin/content/append")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
