from twilio.rest import Client
from flask import session
import random
from models import TempAcc

TWILIO_ACCOUNT_SID = 'ACb78228e61fc41d231e024ee98aba08f9'
TWILIO_AUTH_TOKEN = '49b3c94dc970d1a52d2444d6f30c1f22'
TWILIO_NUMBER = +12014313496


def send_confirmation_code(to_number):
    verification_code = generate_code()
    send_sms(to_number, verification_code)
    session['verification_code'] = verification_code
    return verification_code


def generate_code():
    return str(random.randrange(100000, 999999))


def send_sms(to_number, body):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    twilio_number = TWILIO_NUMBER
    client = Client(account_sid, auth_token)
    client.api.messages.create(to_number, from_=twilio_number, body=body)


def verification(phone_number, otp):
    if TempAcc.objects(toNumber=phone_number, otp=otp):
        TempAcc.objects(toNumber=phone_number).delete()
        return True
    else:
        return False
