from keys import data_encryption_key
from Crypto.Cipher import AES
from Crypto import Random
import jwt

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class AESCipher:
    def __init__(self, key=data_encryption_key[:32]):
        """
        Requires hex encoded param as a key
        """
        self.key = key.decode("hex")

    def encrypt(self, raw):
        """
        Returns hex encoded encrypted value!
        """
        raw = pad(raw)
        iv = "This is a IV456"
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return (iv + cipher.encrypt(raw)).encode("hex")

    def decrypt(self, enc):
        """
        Requires hex encoded param to decrypt
        """
        enc = enc.decode("hex")
        iv = enc[:16]
        enc= enc[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc))

def decrypt(content):
    username = jwt.decode(content, data_encryption_key)
    return username

