from mongoengine import EmailField, IntField, StringField, Document
from mongoengine import DateTimeField, ReferenceField, ListField
from mongoengine import ImageField, BooleanField, DictField, URLField
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, DecimalField
from datetime import datetime, timedelta


class Positions(EmbeddedDocument):
    entryTime = DateTimeField(required=True, default=datetime.now())
    ticker = StringField(required=True)
    quantity = IntField(required=True)
    longPosition = BooleanField(required=True)
    entryPrice = DecimalField(required=True)


class Portfolios(Document):
    portfolioUID = StringField(required=True, unique=True)
    portfolioName = StringField(required=True)
    positionsList = ListField(EmbeddedDocumentField(Positions))
    portfolioStartValue = IntField(required=True)
    cashRemaining = IntField(required=True)

    def save(self, *args, **kwargs):
        if not self.cashRemaining:
            self.cashRemaining = self.portfolioStartValue
        return super(Portfolios, self).save(*args, **kwargs)


class Contests(Document):
    contestUID = StringField(required=True, unique=True)
    contestName = StringField(required=True)
    contestFrequency = IntField(required=True)
    contestStartDate = DateTimeField(required=True, default=datetime.today())
    contestCapacity = IntField(required=True, default=2)
    contestEndDate = DateTimeField(required=True)
    contestPortfolios = ListField(StringField())
    contestEntryFee = IntField(required=True, default=0)
    contestPotSize = IntField(required=True, default=0)
    isPremium = BooleanField(required=True, default=False)
    bucketSizeList = ListField(IntField())
    bucketPrizeList = ListField(IntField())
    vacancies = IntField(required=True)
    portfolioStartValue = IntField(required=True, default=100000)

    def save(self, *args, **kwargs):
        if not self.vacancies:
            self.vacancies = self.contestCapacity
        if not self.contestEndDate:
            self.contestEndDate = self.contestStartDate+timedelta(
                days=self.contestFrequency
                )
        return super(Contests, self).save(*args, **kwargs)


class Customers(Document):
    emailID = EmailField(required=True, unique=True, max_length=300)
    userName = StringField(required=True, unique=True)
    emailVerified = BooleanField(required=True, default=False)
    referralJoinedFrom = StringField(required=True, default="")
    referralCode = StringField(required=True, default="")
    numberReferrals = IntField(required=True, default=0)
    portfoliosActiveID = ListField(ReferenceField(Portfolios))
    contestsActiveID = DictField()
    dateOfBirth = DateTimeField(required=True, default=datetime.today())
    profilePic = URLField(required=True)
    totalQuizWinnings = IntField(required=True, default=0)
    contestRank = IntField(required=True, default=0)
    numArticlesRead = IntField(required=True, default=0)


class Options(EmbeddedDocument):
    value = StringField(required=True)
    isCorrect = IntField(required=True, min_value=0, max_value=1)


class Questions(Document):
    appearancePosition = IntField(required=True, min_value=1, max_value=10)
    theQuestion = StringField(required=True)
    answerOptions = ListField(EmbeddedDocumentField(Options), required=True)
    numResponses = IntField(required=True, default=0)
    numSuccessfulResponses = IntField(required=True, default=0)
    numWatchers = IntField(required=True, default=0)

    def save(self, *args, **kwargs):
        if len(self.answerOptions) > 4:
            raise Exception("InvalidOptionSet")
        return super(Questions, self).save(*args, **kwargs)


class Quiz(Document):
    quizStartTime = DateTimeField(required=True, default=datetime.now())
    quizQuestions = ListField(ReferenceField(Questions), required=True)
    quizParticipants = ListField(StringField())
    quizWinners = ListField(StringField())

    def save(self, *args, **kwargs):
        if len(self.quizQuestions) == 10:
            raise Exception("QuizQuestionsNotEnough")
        return super(Quiz, self).save(*args, **kwargs)


class Content(Document):
    contentHeading = StringField(required=True)
    contentAuthor = StringField(required=True)
    contentPic = URLField(required=True)
    contentTitle = StringField(required=True)
    contentMarkdownLink = URLField(required=True)
    contentHits = IntField(required=True, default=0)
    readingTime = ListField(DateTimeField())

