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


def newsData(token, data):
    tokenValidator = validateToken(token)
    if tokenValidator[1]:
        return encrypt(data_encryption_key, json.dumps(
            {"message": "Unauthorized Request"}
        ).encode('utf-8')), unAuthorized
    else:
        url = decrypt(data_encryption_key, data).decode('utf-8')["url"]
        newurl = fileNameEncoder(url)
        if os.path.exists(os.path.abspath('~/articles')+'/'+newurl):
            fobj = open(os.path.abspath('~/articles')+'/'+newurl)
            data = fobj.read()
            fobj.close()
        else:
            article = Article(url)
            article.download()
            article.parse()
            data = article.text
            fobj = open(os.path.abspath('~/articles')+'/'+newurl, 'w+')
            fobj.write(data)
            fobj.close()
        return encrypt(data_encryption_key, json.dumps(
            {"message": data}
        ).encode('utf-8')), working


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
