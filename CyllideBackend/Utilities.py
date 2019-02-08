import requests
import pandas as pd
from bs4 import BeautifulSoup
import pymongo
import json

def sandp500Fetcher():
    client=pymongo.MongoClient()
    db=client['stocks']
    coll=db['sp500']
    apmj=requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup=BeautifulSoup(apmj.text,"html.parser")
    table=soup.findAll("table")[0].findAll("tr")
    L=[]
    for i in range(1,len(table)):
        ticker=table[i].findAll("td")
        L.append([ticker[0].text,ticker[3].text])
    df=pd.DataFrame(L,columns=["Stock Ticker","Industry"])
    coll.insert_many(df.to_dict('records'))

def expandedListPositions(List):
    Dict={-1:"Short",1:"Long"}
    for i in range(len(List)):
        print(i+1, end =" ")
        print("Stock:{}".format(List[i].stockTicker), end =" ")
        print("Price:{}".format(List[i].entryPrice), end =" ")
        print("Quantity:{}".format(List[i].quantity), end =" ")
        print("Position:{}".format(Dict[List[i].positionType]))

