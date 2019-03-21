from Crypto.Cipher import AES
from keys import data_encryption_key
import base64


def encrypt(message):
    obj = AES.new(data_encryption_key, AES.MODE_CBC, 'This is an IV456')
    ciphertext = obj.encrypt(message)
    return base64.encodebytes(ciphertext)


def decrypt(ciphertext):
    ciphertext = base64.decodebytes(ciphertext)
    obj2 = AES.new(data_encryption_key, AES.MODE_CBC, 'This is an IV456')
    message = obj2.decrypt(ciphertext)
    return message
