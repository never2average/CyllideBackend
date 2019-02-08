import requests as rq
from email_templates import sendVerificationEmail
from email_templates import passwordResetEmail as pREmail
from prizeDistribution import getReturns,calculateEntryFee,getWinnerNo
from models import Users,Contests,Portfolios,Positions
from datetime import datetime,timedelta
from mongoengine.queryset.visitor import Q
import bcrypt,pytz,time
from keys import secretKey,specialDecoder
import jwt,json,requests
import mongoengine
mongoengine.connect('TradeRoyale')
from random import randint
import pymongo
from google.oauth2 import id_token
from google.auth.transport import requests

def passwordResetEmail(email,name,browser,osName):
    return pREmail(email,name,browser,osName)

def getCurrentPrice(stockTicker):
    return 500-sum([ord(c) for c in stockTicker])/randint(1,6)

def loginConnector(email,password):
    try:
        user=Users.objects.get(emailID=email)
        if user.password==bcrypt.hashpw(password.encode('UTF-8'),user.password):
            token=jwt.encode({"user":user.emailID,"exp":datetime.utcnow()+timedelta(days=30)},secretKey)
            return {"token":token.decode('UTF-8')}
        else:
            return {"error":"PasswordsDonotMatch"}
    except:
        return {"error":"User does not exist"}

def signupConnector(firstName,lastName,email,password):
    try:
        user=Users.objects.get(emailID=email)
        return {"error":"Email Id Already Exists"+user.emailID}
    except:
        password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        user=Users(
            firstName=firstName,emailID=email,lastName=lastName,password=password,
            global_rank=Users.objects.count()+1
            )
        user.save()
        sendVerificationEmail(email,firstName)
        token=jwt.encode({"user":user.emailID,"exp":datetime.utcnow()+timedelta(hours=24)},secretKey)
        return {"token":token.decode('UTF-8')}

def processVerificationToken(token):
    try:
        token=json.loads(token)
        email=jwt.decode(token,secretKey)["user"]
        user=Users.objects.get(emailID=email)
        return user.emailID
    except:
        return "error"

def getUserDetails(email,*varargs,**kwargs):
    try:
        user=json.loads(Users.objects.get(emailID=email).to_json())
        if kwargs!={}:
            return user
        
        details=[]
        for i in varargs:
            details.append(user[i])

        if len(details)==1:
            return details[0]
        return details

    except:
        raise Exception("UserDoesNotExist")

def verifiedEmail(link):
    try:
        email=specialDecoder(link)
        try:
            user=Users.objects.get(emailID=email)
            user.update(set__emailVerified=True)
            return "Successfully Verified Email"
        except:
            raise Exception("EmailNotFound")
    except:
        raise Exception("InvalidURLEntered")

def getLookbackandFreq(timespan):
    if timespan=="1 day":
        return "2m","1d"
    elif timespan=="5 days":
        return "15m","5d"
    elif timespan=="1 month":
        return "30m","1mo"
    elif timespan=="6 months":
        return "1d","6mo"
    elif timespan=="YTD":
        return "1d","ytd"
    elif timespan=="1 year":
        return "1d","1y"
    elif timespan=="5 years":
        return "1wk","1y"

def parseDates(datelist):
    newList=[]
    tz=pytz.timezone('Asia/Kolkata')
    for i in datelist:
        newList.append(tz.localize(datetime.fromtimestamp(i)).strftime("%X"))
    return newList


def getData(ticker,timespan="1 Day",attribute="close"):
    attribute=attribute.lower()
    freq,lookback=getLookbackandFreq(timespan)
    url="""https://query1.finance.yahoo.com/v8/finance/chart/{}?
    region=US&lang=en-US&includePrePost=false&interval={}&range={}
    &corsDomain=finance.yahoo.com&.tsrc=finance""".format(ticker,freq,lookback)
    data=requests.get(url).text
    data=json.loads(data)["chart"]["result"][0]
    return {"timestamp":parseDates(data["timestamp"]),"attribute":data["indicators"]["quote"][0][attribute]}

def calcEntryFee(participants,prizepool):
    entryFee=calculateEntryFee(prizepool,participants,getReturns(prizepool,participants))
    return {"entryFee":entryFee}

def getContestName(email):
    contestNames=getUserDetails(email,"contestsActiveID")
    String=""
    for i in contestNames.keys():
        String+=contestNames[i]+"<br>"
    return String

colormap={"1":"orange","7":"#3b5998","30":"#128c7e"}

def calculatePortfolioReturns(positionsList,portfolioValue,cashRemaining):
    currentValue=cashRemaining
    for i in positionsList:
        currentValue+=getCurrentPrice(i.ticker)*i.quantity
    return round(100*(currentValue/portfolioValue-1),2)

def jsonifyContest(contest):
    return {
        "contestName":contest.contestName,
        "contestEntryFee":contest.contestEntryFee,
        "contestFrequency":contest.contestFrequency,
        "contestStartDate":contest.contestStartDate,
        "contestEndDate":contest.contestEndDate,
        "contestCapacity":contest.contestCapacity,
        "contestPotSize":contest.contestPotSize,
        "vacancies":contest.vacancies,
        "winners":getWinnerNo(contest.contestPotSize,contest.contestCapacity),
        "identifier":colormap[str(contest.contestFrequency)]
        }


def minimalContestData(frequency):
    con=list(Contests.objects(Q(contestFrequency=frequency) & Q(contestEndDate__gte=datetime.now())))
    n=len(con)
    contestDict={}
    for i in range(n):
        contestDict[con[i].contestUID]=jsonifyContest(con[i])
    return contestDict

def minJsonifyPortfolios(portfolio):
    return {
        "portfolioName":portfolio.portfolioName,
        "portfolioReturns":calculatePortfolioReturns(
            portfolio.positionsList,portfolio.portfolioStartValue,
            portfolio.cashRemaining
            ),
        "portfolioRank":"-"
    }

def minimalPortfolioDict(UID):
    UID=json.loads(UID)
    con=Contests.objects.get(contestUID=UID)
    minportfolios={}
    for i in con.contestPortfolios:
        minportfolios[i.portfolioUID]=minJsonifyPortfolios(i)
    return minportfolios

def debug():
    # pos1=Positions(
    #     ticker="AAPL",
    #     quantity=10,
    #     longPosition=True
    # )
    # pos1.save()
    
    # pos2=Positions(
    #     ticker="TSLA",
    #     quantity=10,
    #     longPosition=False
    # )
    # pos2.save()
    
    # port=Portfolios(
    #     portfolioName="priyesh_t1",
    #     portfolioUID="stock_royale_t1",
    #     portfolioStartValue=100000,
    #     positionsList=[pos1,pos2]
    # )
    # port.save()

    # con=Contests(
    #     contestUID="new_contest_2",contestName="Stock Royale Daily",contestFrequency=1,
    #     contestPotSize=84,contestEntryFee=2,bucketSizeList=[1],bucketPrizeList=[16],
    #     contestCapacity=50
    #     )
    # con.save()
    # con2=Contests(
    #     contestUID="new_contest_3",contestName="Stock Royale Weekly",contestFrequency=7,
    #     contestPotSize=210,contestEntryFee=5,bucketSizeList=[1],bucketPrizeList=[16],
    #     contestCapacity=50
    #     )
    # con2.save()
    con3=Contests(
        contestUID="new_contest_5",contestName="Stock Royale Monthly",contestFrequency=30,
        contestPotSize=6720,contestEntryFee=80,bucketSizeList=[1],bucketPrizeList=[16],
        contestCapacity=100
        )
    con3.save()
    con4=Contests(
        contestUID="new_contest_6",contestName="Stock Royale Monthly",contestFrequency=30,
        contestPotSize=6720,contestEntryFee=80,bucketSizeList=[1],bucketPrizeList=[16],
        contestCapacity=100
        )
    con4.save()
    con5=Contests(
        contestUID="new_contest_7",contestName="Stock Royale Monthly",contestFrequency=30,
        contestPotSize=6720,contestEntryFee=80,bucketSizeList=[1],bucketPrizeList=[16],
        contestCapacity=100
        )
    con5.save()
    # con2=Contests(
    #     contestUID="new_contest_2",contestName="Stock Royale Deluxe",contestFrequency=1
    #     ,contestPotSize=500,contestEntryFee=275,contestEndDate=datetime.now(),bucketSizeList=[1],bucketPrizeList=[500]
    #     )
    # con2.save()
    # print(loginConnector("priyesh.sriv2017+test@gmail.com","password"))
    # con=Contests(
    #     contestUID="new_contest_4",contestName="Stock Royale Mega",contestFrequency=7,contestCapacity=5,
    #     contestPotSize=1200,contestEntryFee=245,bucketSizeList=[1,1],bucketPrizeList=[800,400]
    #     )
    # con.save()
    # return minimalContestData(1)

def getContestData(uid,*varargs,**kwargs):
    try:
        uid=json.loads(uid)
        contest=Contests.objects.get(contestUID=uid)
        data=[]
        if kwargs!={}:
            return contest

        for i in varargs:
            if i=="contestWinners":
                data.append(getWinnerNo(contest["contestPotSize"],contest["contestCapacity"]))
                continue
            data.append(contest[i])

        if len(data)==1:
            return data[0]
        return data

    except:
        return "invalid"

def basicData(num_stocks):
    cl=pymongo.MongoClient()
    db=cl["stocks"]
    coll=db['sp500']
    data={}
    for i in list(coll.find().limit(num_stocks)):
        ticker=i["Stock Ticker"]
        data[ticker]=[round(getCurrentPrice(ticker),2),round(100*randint(-1,1)/randint(1,30),2)]
    return data

def basicRegexData(regex,num_stocks):
    cl=pymongo.MongoClient()
    regex=json.loads(regex)
    print(regex)
    db=cl["stocks"]
    coll=db['sp500']
    data={}
    for i in list(coll.find({"Stock Ticker":{"$regex":regex}}).limit(num_stocks)):
        ticker=i["Stock Ticker"]
        data[ticker]=[round(getCurrentPrice(ticker),2),round(100*randint(-1,1)/randint(1,30),2)]
    return data

def pushIntoDB(UID,email,data,name,cashRemaining):
    UID=json.loads(UID)
    contest=Contests.objects.get(contestUID=UID)
    if datetime.now()<contest.contestEndDate:
        if contest.vacancies>0:
            user=Users.objects.get(emailID=email)
            if user.accountBalance<contest.contestEntryFee:
                return "InsufficientBalance"
            else:
                contest.update(set__vacancies=contest.vacancies-1)
                port=Portfolios(
                    portfolioUID=email+"_"+name+"_"+UID+"_"+str(time.time()),
                    portfolioName=name,
                    portfolioStartValue=contest.portfolioStartValue)
                port.save()
                contest.update(add_to_set__contestPortfolios=[port])
                port.update(set__cashRemaining=int(float(cashRemaining)))
                for i in data:
                    if i["positionType"]==1:
                        longPos=True
                    else:
                        longPos=False
                    pos=Positions(
                        ticker=i["ticker"],
                        quantity=i["quantity"],
                        longPosition=longPos,
                        entryPrice=i["currentPrice"]
                    )
                    pos.save()
                    port.update(add_to_set__positionsList=[pos])
                user.update(set__accountBalance=user.accountBalance-contest.contestEntryFee)
                user.update(add_to_set__portfoliosActiveID=[port])
                return "PushSuccessful"
        return "ContestFull"
    return "ContestFinished"

def loginfb(token, firstName, emailID):
    try:
        clientId="330603044186569"
        clientSecret="0423c238ce84a5b3d7a0ac9781bebd12"
        appLink="https://graph.facebook.com/oauth/access_token?client_id=" + clientId + "&client_secret=" + clientSecret + "&grant_type=client_credentials"
        appToken = json.loads(rq.get(appLink).text)['access_token']
        response=rq.get("https://graph.facebook.com/debug_token?input_token="+token+"&access_token="+appToken)
        userid = json.loads(response.text)['data']['user_id']
        try:
            user=Users.objects.get(emailID=emailID)
            token=jwt.encode({"user":user.emailID,"exp":datetime.utcnow()+timedelta(days=30)},secretKey)
            return {"token":token.decode('UTF-8'), "newUser": False}
        except Exception as e:
            password=userid+"Thissfecre2343j8dsa8**1f"
            password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            user=Users(firstName=firstName,emailID=emailID,password=password)
            user.save()
            token=jwt.encode({"user":user.emailID,"exp":datetime.utcnow()+timedelta(days=30)},secretKey)
            return {"token":token.decode('UTF-8'), "newUser":True}
    except Exception as e:
        print(e)
        return {"error":"Unable to sign in through facebook."}

def googlesignin(token, firstName, emailID):
    request = requests.Request()
    idinfo = id_token.verify_oauth2_token(token,request)
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        print("Could not find issuer")
        raise ValueError('Wrong issuer')
    try:
        user=Users.objects.get(emailID=emailID)
        token=jwt.encode({"user":user.emailID,"exp":datetime.utcnow()+timedelta(days=30)},secretKey)
        return {"token":token.decode('UTF-8'), "newUser": False}
    except:
        password=idinfo['sub']+"Thissfecre2343j8dsa8**1f"
        password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        user=Users(firstName=firstName,emailID=emailID,password=password)
        user.save()
        token=jwt.encode({"user":user.emailID,"exp":datetime.utcnow()+timedelta(days=30)},secretKey)
        return {"token":token.decode('UTF-8')}

if __name__=="__main__":
    debug()
    # print(getData("FB"))
    # print(basicRegexData(json.dumps("AA"),5))
    # minimalPortfolioDict(json.dumps("new_contest_3"))
    # print(minimalPortfolioDict(json.dumps("new_contest_3")))