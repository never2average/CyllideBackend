import sys
import unittest
sys.path.insert(0, '/Users/notAnshuman/CyllideBackend/CyllideBackend/')
from forumConnectors import *
from keys import data_encryption_key
from simplecrypt import decrypt, encrypt
from adminConnectors import adminLogin


class forumConnectorsTest(unittest.TestCase):
    def test_add_query(self):
        token = adminLogin(
            "prasannkumar1263@gmail.com",
            "prasannkumar1263"
            )[0]["token"]
        self.assertEqual(
            decrypt(data_encryption_key, addQuery(token, encrypt(data_encryption_key, "Lool"))[0]),
            {"message": "Quiz Posted Sucessfully"}
            )


if __name__ == '__main__':
    unittest.main()