import jwt
from keys import secret_key
from models import Customers
from newspaper import Article
import string
import os
from statuscodes import unAuthorized, working


def newsData(token, url):
    tokenValidator = validateToken(token)
    if tokenValidator[1]:
        return {"message": "Unauthorized Request"}, unAuthorized
    else:
        newurl = fileNameEncoder(url)
        if os.path.exists('articles/'+newurl):
            fobj = open('articles/'+newurl)
            data = fobj.read()
            fobj.close()
        else:
            article = Article(url)
            article.download()
            article.parse()
            data = article.text
            fobj = open('articles/'+newurl, 'w')
            fobj.write(data)
            fobj.close()
        return {"message": data}, working


def fileNameEncoder(url):
    table = str.maketrans({key: None for key in string.punctuation})
    return url.translate(table)


def validateToken(token):
    try:
        username = jwt.decode(token, secret_key)["user"]
        try:
            cust = Customers.objects.get(userName=username)
            return cust.userName, True
        except:
            return None, False
    except:
        return None, False

# if __name__ == "__main__":
#     url = 'https://timesofindia.indiatimes.com/entertainment/events/hyderabad/queer-carnival-2019-ended-on-a-gay-note-in-the-city/articleshow/67977823.cms'
#     print(newsData("token", url))
#     print(newsData('token', url))
