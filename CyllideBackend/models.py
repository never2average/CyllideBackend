from mongoengine import IntField, StringField, Document
from mongoengine import DateTimeField, ReferenceField, DecimalField
from mongoengine import EmbeddedDocument, EmbeddedDocumentListField, ListField
from mongoengine import BooleanField, URLField
from datetime import datetime, timedelta


class Positions(EmbeddedDocument):
    entryTime = DateTimeField(required=True, default=datetime.now())
    ticker = StringField(required=True)
    quantity = IntField(required=True)
    longPosition = BooleanField(required=True)
    entryPrice = DecimalField(required=True)
    state = StringField(required=True, default="Pending", choices=["Pending","Holding", "Closed"])


class Portfolios(Document):
    portfolioOwner = StringField(required=True)
    portfolioName = StringField(required=True)
    portfolioCapex = StringField(required=True, choices=["smallcap", "midcap", "largecap", "nifty500"])
    positionsList = EmbeddedDocumentListField(Positions, required=True)
    portfolioStartValue = IntField(required=True)
    cashRemaining = IntField(required=True)

    def save(self, *args, **kwargs):
        if not self.cashRemaining:
            self.cashRemaining = self.portfolioStartValue
        return super(Portfolios, self).save(*args, **kwargs)


class Contests(Document):
    contestName = StringField(required=True)
    contestPortfolios = ListField(StringField())
    contestEntryFee = IntField(required=True, default=0)
    contestCapex = StringField(required=True, choices=["smallcap", "midcap", "largecap", "nifty500"])
    portfolioStartValue = IntField(required=True, default=100000)
    signUps = IntField(required=True, default=0)


class Customers(Document):
    userName = StringField(required=True, unique=True)
    phoneNumber = IntField(required=True, unique=True, max_length=10)
    referralJoinedFrom = StringField(required=True, default="")
    referralCode = StringField(required=True, default="")
    numberReferrals = IntField(required=True, default=0)
    portfoliosActiveID = ListField(ReferenceField(Portfolios))
    contestsActiveID = ListField(ReferenceField(Contests))
    dateOfBirth = DateTimeField(required=True, default=datetime.today())
    profilePic = URLField(
        required=True,
        default="https://www.freeiconspng.com/uploads/profile-icon-9.png"
        )
    totalQuizWinnings = IntField(required=True, default=0)
    contestRank = IntField(required=True, default=0)
    numArticlesRead = IntField(required=True, default=0)
    numCoins = IntField(required=True, default=0)

    def save(self, *args, **kwargs):
        if not self.referralCode:
            self.referralCode = self.userName+"user"
        super(Customers, self).save(*args, **kwargs)


class Options(EmbeddedDocument):
    value = StringField(required=True)
    isCorrect = IntField(required=True, min_value=0, max_value=1)
    numResponses = IntField(required=True, default=0)


class Questions(Document):
    appearancePosition = IntField(required=True, min_value=1, max_value=10)
    theQuestion = StringField(required=True)
    answerOptions = EmbeddedDocumentListField(Options, required=True)
    numResponses = IntField(required=True, default=0)
    numSuccessfulResponses = IntField(required=True, default=0)
    numWatchers = IntField(required=True, default=0)

    def save(self, *args, **kwargs):
        if len(self.answerOptions) > 4:
            raise Exception("InvalidOptionSet")
        super(Questions, self).save(*args, **kwargs)


class Quiz(Document):
    quizStartTime = DateTimeField(required=True, default=datetime.now())
    quizQuestions = ListField(ReferenceField(Questions), required=True)
    quizParticipants = ListField(StringField())
    quizWinners = ListField(StringField())

    def save(self, *args, **kwargs):
        if len(self.quizQuestions) != 10:
            raise Exception("QuizQuestionsNotEnough")
        else:
            super(Quiz, self).save(*args, **kwargs)


class Content(Document):
    contentAuthor = StringField(required=True)
    contentPic = URLField(required=True)
    contentType = StringField(
        required=True,
        choices=[
            "Legends of the Game",
            "Case Studies",
            "Stories"
            ]
        )
    contentTitle = StringField(required=True)
    contentMarkdownLink = URLField(required=True)
    contentHits = IntField(required=True, default=0)
    readingTime = ListField(DateTimeField())


class Answer(Document):
    answerUpvotes = IntField(required=True, default=0)
    answerBody = StringField(required=True)
    answerUID = StringField(required=True)
    answerTime = DateTimeField(required=True, default=datetime.now())


class Comment(EmbeddedDocument):
    commentBody = StringField(required=True)
    commentUID = StringField(required=True)
    commentTime = DateTimeField(required=True, default=datetime.now())


class Query(Document):
    queryNumViews = IntField(required=True, default=0)
    commentList = EmbeddedDocumentListField(Comment, default=[])
    queryBody = StringField(required=True)
    answerList = ListField(ReferenceField(Answer))
    isAnswered = BooleanField(required=True, default=False)
    isClosed = BooleanField(required=True, default=False)
    queryTime = DateTimeField(required=True, default=datetime.now())
    queryUID = StringField(required=True)
    queryLastUpdateTime = DateTimeField(required=True)
    queryTags = ListField(StringField(
            choices=[
                "Business",
                "Finance",
                "Stock Markets",
                "Macro-Economics"
                ]
            ))

    def save(self, *args, **kwargs):
        if not self.queryLastUpdateTime:
            self.queryLastUpdateTime = self.queryTime
        super(Query, self).save(*args, **kwargs)


class TempAcc(Document):
    toNumber = IntField(required=True)
    otp = IntField(required=True, min_value=100000, max_value=999999)
    username = StringField(required=True)
