import jwt
from keys import secret_key, data_encryption_key
from models import Customers
from newspaper import Article
import string
import os
import json
from statuscodes import unAuthorized, working
from simplecrypt import decrypt, encrypt
from srblib import abs_path


def newsData(token, url):
    tokenValidator = validateToken(token)
    if tokenValidator[1]:
        return json.dumps(
            {"message": "Unauthorized Request"}
        ), unAuthorized
    else:
        newurl = fileNameEncoder(url)
        if os.path.exists(abs_path('~/articles')+'/'+newurl):
            fobj = open(abs_path('~/articles')+'/'+newurl)
            data = fobj.read()
            fobj.close()
        else:
            article = Article(url)
            article.download()
            article.parse()
            data = article.text
            fobj = open(abs_path('~/articles')+'/'+newurl, 'w+')
            fobj.write(data)
            fobj.close()
        return json.dumps(
            {"message": data}
        ), working


def fileNameEncoder(url):
    table = str.maketrans({key: None for key in string.punctuation})
    return url.translate(table)


def validateToken(token):
    try:
        username = jwt.decode(token, secret_key)["user"]
        try:
            cust = Customers.objects.get(userName=username)
            return cust.userName, True
        except Exception:
            return None, False
    except Exception:
        return None, False
