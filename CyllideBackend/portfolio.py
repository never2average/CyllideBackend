from Utilities import expandedListPositions
from random import randint

pos=[]

def getCurrentPrice(stockTicker):
    return 500-sum([ord(c) for c in stockTicker])/randint(1,6)

class ExcessQuantityException(Exception):
    def __init__(self,message):
        self.message=message

class Position:
    def __init__(self,stockTicker,entryPrice,quantity,positionType):
        self.stockTicker=stockTicker
        self.entryPrice=entryPrice
        self.positionType=positionType
        self.quantity=quantity
    def exitPosition(self,exitPrice,quantity):
        if self.quantity>=quantity:
            self.quantity-=quantity
            netReturn=quantity*self.positionType*(exitPrice-self.entryPrice)
        elif self.quantity<quantity:
            self.quantity=quantity-self.quantity
            self.positionType*=-1
            netReturn=quantity*self.positionType*(exitPrice-self.entryPrice)
            self.entryPrice=exitPrice
        return netReturn
    def addToPosition(self,entryPrice,quantity):
        self.entryPrice=(self.entryPrice+entryPrice)/(self.quantity+quantity)
        self.quantity+=quantity


class Order:
    def __init__(self,stockTicker,quantity,orderType,action,executionPrice=None):
        self.stockTicker=stockTicker
        self.action=action
        self.orderType=orderType
        self.quantity=quantity
        self.executionPrice=executionPrice
        self.getExecutionPrice()
    def getExecutionPrice(self):
        if self.executionPrice==None:
            self.executionPrice=getCurrentPrice(self.stockTicker)
    def execute(self,positionList):
        index=-1
        for i in range(len(positionList)):
            if positionList[i].stockTicker==self.stockTicker:
                index=i
                break
        if index==-1:
            positionList.append(Position(self.stockTicker,self.executionPrice,self.quantity,self.action))
        
        else:    
            pos=positionList[index]
            if(self.action==pos.positionType):
                pos.addToPosition(self.executionPrice,self.quantity)
            if (self.action==-pos.positionType):
                pos.exitPosition(self.executionPrice,self.quantity)
            positionList[index]=pos


class Portfolio:
    def __init__(self,competitionName,userName,portfolioBalance,portfolioName):
        self.positionList=[]
        self.registeredCompetition=competitionName
        self.portfolioOwner=userName
        self.portfolioBalance=portfolioBalance
        self.portfolioName=portfolioName
        self.portfolioUID=self.portfolioName+"_"+self.registeredCompetition+"_"+self.portfolioOwner
    def takeOrder(self,order):
        if order.orderType=="MARKET":
            order.execute(self.positionList)

    
while True:
    inp=input()
    if inp == "n":
        break
    params=input().split(" ")
    if len(params)==4:
        order=Order(params[0],int(params[1]),params[2],int(params[3]))
    else:
        order=Order(params[0],int(params[1]),params[2],int(params[3]),int(params[4]))
    order.execute(pos)

expandedListPositions(pos)