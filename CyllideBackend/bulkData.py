import json
from bs4 import BeautifulSoup
import datetime
import requests
from subprocess import PIPE, run
home = "/home/ubuntu/data"


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
        "details":  getDetails(niftySubset),
        "summary":  getSummary(niftySubset)
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
        {"class":  "qsp-2col-profile Mt(10px) smartphone_Mt(20px) Lh(1.7)"}
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
    try:
        fobj = open(
            home+"/"+'_'.join(tickerList) + "_DET_" + str(dobj.year) + '.json'
        )
        return json.load(fobj)
    except Exception:
        Dict = {}
        for i in tickerList:
            Dict[i] = getDetailsAct(i)
        fobj = open(
            home+"/"+'_'.join(tickerList) + "_DET_" + str(dobj.year) + '.json',
            "w"
        )
        json.dump(Dict, fobj)
        fobj.close()
        return Dict


def getSummary(tickerList):
    Dict = {}
    dobj = datetime.date.today()
    try:
        fobj = open(
            home+"/"+'_'.join(tickerList) + dobj.strftime("%d%B%Y") + '.json'
        )
        return json.load(fobj)
    except Exception:
        Dict = {}
        for ticker in tickerList:
            page = requests.get(
                "https://in.finance.yahoo.com/quote/{}.NS?p={}.NS".format(
                    ticker, ticker
                )
            ).text
            soup = BeautifulSoup(page, "html.parser")
            tables = soup.find_all("table", {"class":  "W(100%)"})
            incStData = []
            for i in tables:
                tbody = i.tbody
                trows = tbody.find_all("td")
                for i in trows:
                    incStData.append(i.text)
            n = len(incStData)
            Dict[ticker] = {}
            for i in range(0, n, 2):
                if incStData[i] in [
                    "PE ratio (TTM)", "Open",
                    "Market cap", "Previous close"
                ]:
                    Dict[ticker][incStData[i]] = incStData[i+1]
        fobj = open(
            home+"/"+'_'.join(tickerList) + dobj.strftime("%d%B%Y") + '.json',
            "w"
        )
        json.dump(Dict, fobj)
        fobj.close()
        return Dict


companyIDs = {
    "TCS": 8345,
    "INFY": 10960,
    "RELIANCE": 13215,
    "ONGC": 11599,
    "ZEEL": 11769,
    "TATAMOTORS": 12934,
    "YESBANK": 16552,
    "INDUSINDBK": 9196,
    "VEDL": 13111,
    "JSWSTEEL": 8352,
    "UPL": 6114,
    "HCLTECH": 4291,
    "TATASTEEL": 12902,
    "ICICIBANK": 9194,
    "IOC": 11924,
    "HEROMOTOCO": 13636,
    "GRASIM": 13696,
    "CIPLA": 13917,
    "BAJFINANCE": 11260,
    "SBIN": 11984,
    "HINDALCO": 13637,
    "TITAN": 12903,
    "INFRATEL": 22411,
    "HDFCBANK": 9195,
    "KOTAKBANK": 12161,
    "NTPC": 12316,
    "ASIANPAINT": 14034,
    "WIPRO": 12799,
    "ITC": 13554,
    "ADANIPORTS": 20316,
    "MARUTI": 11890,
    "AXISBANK": 9175,
    "EICHERMOT": 13787,
    "BHARTIARTL": 2718,
    "BAJAJ-AUTO": 21430,
    "HDFC": 13640,
    "COALINDIA": 11822,
    "ULTRACEMCO": 3027,
    "POWERGRID": 4628,
    "GAIL": 4845,
    "BAJAJFINSV": 21426,
    "BRITANNIA": 13934,
    "LT": 13447,
    "BPCL": 11941,
    "HINDUNILVR": 13616,
    "TECHM": 11221,
    "DRREDDY": 13841,
    "M&M": 11898,
    "SUNPHARMA": 9134,
    "IBULHSGFIN": 15580
}


def ohlcBulkData():
    try:
        filename = run(
            "ls -t {}/ohlc_nifty_* | head -1",
            stdout=PIPE, stderr=PIPE,
            shell=True
        )
        fobj = open(filename.stdout, "r")
        return fobj.read(), 200
    except Exception:
        ohlc = {}
        timestamp = datetime.datetime.now().strftime("%s")
        timestamp = int(timestamp) * 1000
        s = "https://json.bselivefeeds.indiatimes.com/ET_Community/companypagedata?companyid={}&_={}"
        for i in companyIDs:
            r = requests.get(s.format(companyIDs[i], timestamp)).json()
            ohlc[i] = r["bseNseJson"][1]["lastTradedPrice"]
        json.dump(
            ohlc,
            open(home + "/ohlc_nifty_{}.json".format(timestamp), "w+")
        )
        return json.dumps(ohlc), 200
