import json
from bs4 import BeautifulSoup
import datetime
import requests
home = "/home/ubuntu"


nifty50 = [
    "TCS", "INFY", "RELIANCE", "ONGC", "ZEEL", "TATAMOTORS",
    "YESBANK", "INDUSINDBK", "VEDL", "JSWSTEEL", "UPL", "HCLTECH",
    "TATASTEEL", "ICICIBANK", "IOC", "HEROMOTOCO", "GRASIM",
    "CIPLA", "BAJFINANCE", "SBIN", "HINDALCO", "TITAN", "INFRATEL",
    "HDFCBANK", "KOTAKBANK", "NTPC", "ASIANPAINT", "WIPRO", "ITC",
    "ADANIPORTS", "MARUTI", "AXISBANK", "EICHERMOT", "BHARTIARTL",
    "BAJAJ-AUTO", "HDFC", "COALINDIA", "ULTRACEMCO", "POWERGRID",
    "GAIL", "BAJAJFINSV", "BRITANNIA", "LT", "BPCL", "HINDUNILVR",
    "TECHM", "DRREDDY", "M&M", "SUNPHARMA", "IBULHSGFIN"
]


def processData(pageNo):
    pageNo = int(pageNo)
    niftySubset = nifty50[(pageNo-1)*10:10*pageNo:]
    bulkData = {
        "details": getDetails(niftySubset),
        "summary": getSummary(niftySubset)
    }
    return json.dumps(bulkData), 200


def getDetailsAct(ticker):
    page = requests.get(
        "https://in.finance.yahoo.com/quote/{}.NS/profile?p={}.NS".format(
            ticker,  ticker
        )
    ).text
    soup = BeautifulSoup(page, "html.parser")
    divs = soup.find_all(
        "div",
        {"class": "qsp-2col-profile Mt(10px) smartphone_Mt(20px) Lh(1.7)"}
    )
    for i in divs:
        mydiv = i
        break
    Dict = {}
    paras = mydiv.findAll("p")
    count = 0
    for i in paras:
        if count != 0:
            spans = i.findAll("span")
            data = []
            for j in spans:
                data.append(j.text)
            n = len(data)
            for i in range(0, n-2, 2):
                if data[i] in ["Sector", "Industry"]:
                    Dict[data[i]] = data[i+1]
        count += 1
    return Dict


def getDetails(tickerList):
    dobj = datetime.datetime.today()
    # try:
    fobj = open(
        home+"/"+'_'.join(tickerList) + "_DET_" + str(dobj.year) + '.json'
    )
    return json.loads(fobj)
    # except Exception:
    #     Dict = {}
    #     for i in tickerList:
    #         Dict[i] = getDetailsAct(i)
    #     fobj = open(
    #         home+"/"+'_'.join(tickerList) + "_DET_" + str(dobj.year) + '.json',
    #         "w"
    #     )
    #     json.dump(Dict, fobj)
    #     fobj.close()
    #     return Dict


def getSummary(tickerList):
    Dict = {}
    dobj = datetime.date.today()
    # try:
    fobj = open(
        home+"/"+'_'.join(tickerList) + dobj.strftime("%d%B%Y") + '.json'
    )
    return json.loads(fobj)
    # except Exception:
    #     Dict = {}
    #     for ticker in tickerList:
    #         page = requests.get(
    #             "https://in.finance.yahoo.com/quote/{}.NS?p={}.NS".format(
    #                 ticker, ticker
    #             )
    #         ).text
    #         soup = BeautifulSoup(page, "html.parser")
    #         tables = soup.find_all("table", {"class": "W(100%)"})
    #         incStData = []
    #         for i in tables:
    #             tbody = i.tbody
    #             trows = tbody.find_all("td")
    #             for i in trows:
    #                 incStData.append(i.text)
    #         n = len(incStData)
    #         Dict[ticker] = {}
    #         for i in range(0, n, 2):
    #             if incStData[i] in [
    #                 "PE ratio (TTM)", "Open",
    #                 "Market cap", "Previous close"
    #             ]:
    #                 Dict[ticker][incStData[i]] = incStData[i+1]
    #     fobj = open(
    #         home+"/"+'_'.join(tickerList) + dobj.strftime("%d%B%Y") + '.json',
    #         "w"
    #     )
    #     json.dump(Dict, fobj)
    #     fobj.close()
    #     return Dict
