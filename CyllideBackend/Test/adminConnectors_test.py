import unittest
import sys
sys.path.insert(0, '/Users/notAnshuman/CyllideBackend/CyllideBackend/')
from adminConnectors import *


class adminConnectorsTest(unittest.TestCase):
    def test_validate_token(self):
        token = adminLogin("prasannkumar1263@gmail.com", "prasannkumar1263")[0]["token"]
        self.assertEqual(validateToken(token),True)
        self.assertEqual(validateToken("lofjdosa"),False)

    def test_user_count(self):
        token = adminLogin("prasannkumar1263@gmail.com", "prasannkumar1263")[0]["token"]
        self.assertEqual(getUserCount(token)[0]["numUsers"],0)

    def test_add_quiz(self):
        token = adminLogin("prasannkumar1263@gmail.com", "prasannkumar1263")[0]["token"]
        self.assertEqual(addQuiz(token, {
    "start_date": "Aug 28 1999 12:00AM",
    "questions":
    [
        {
            "question": "Who the fuck?",
            "options": {"A": 0, "B": 1, "C": 0, "D": 0}
        },
        {
            "question": "Who the fuck?",
            "options": {"A": 0, "B": 1, "C": 0, "D": 0}
        },
        {
            "question": "Who the fuck?",
            "options": {"A": 0, "B": 1, "C": 0, "D": 0}
        },
        {
            "question": "Who the fuck?",
            "options": {"A": 0, "B": 1, "C": 0, "D": 0}
        },
        {
            "question": "Who the fuck?",
            "options": {"A": 0, "B": 1, "C": 0, "D": 0}
        },
        {
            "question": "Who the fuck?",
            "options": {"A": 0, "B": 1, "C": 0, "D": 0}
        },
        {
            "question": "Who the fuck?",
            "options": {"A": 0, "B": 1, "C": 0, "D": 0}
        },
        {
            "question": "Who the fuck?",
            "options": {"A": 0, "B": 1, "C": 0, "D": 0}
        },
        {
            "question": "Why the fuck?",
            "options": {"A": 0, "B": 0, "C": 1, "D": 0}
        },
        {
            "question": "Why the fuck?",
            "options": {"A": 0, "B": 0, "C": 1, "D": 0}
        }
    ]
})[0], {"message": "QuizAddedSuccessfully"})

    def test_add_contest(self):
        token = adminLogin("prasannkumar1263@gmail.com", "prasannkumar1263")[0]["token"]
        self.assertEqual(addContest(token,{
    "name": "Stock Stand-off",
    "frequency": 1,
    "start_date": "Aug 28 1999 12:00AM",
    "isPremium": False,
    "capacity": 20
})[0],{"message": "ContestAddedSuccessfully"})
        


if __name__ == '__main__':
    unittest.main()
