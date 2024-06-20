import os
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()
class notmgr:
    def __init__(self):
        self.client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_AUTH_TOKEN"])

    def sms(self, msg):
        message = self.client.messages.create(
            from_=os.environ["TWILIO_VIRTUAL_NUMBER"],
            body=msg,
            to=os.environ["TWILIO_VERIFIED_NUMBER"]
        )
        print(message.sid)

    def whatsapp(self, msg):
        message = self.client.messages.create(
            from_=f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',
            body=msg,
            to=f'whatsapp:{os.environ["TWILIO_VERIFIED_NUMBER"]}'
        )
        print(message.sid)