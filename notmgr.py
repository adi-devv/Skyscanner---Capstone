import os, smtplib
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()
class notmgr:
    def __init__(self):
        self.client = Client(os.environ["TWILIO_SID"], os.environ["TWILIO_AUTH_TOKEN"])
        self.client = Client(os.environ['TWILIO_SID'], os.environ["TWILIO_AUTH_TOKEN"])
        self.email = os.environ['mymail']
        self.pwd = os.environ['mpass']

    def notify(self, msg, list):
        self.client.messages.create(
            from_=os.environ["TWILIO_VIRTUAL_NUMBER"],
            body=msg,
            to=os.environ["TWILIO_VERIFIED_NUMBER"]
        )

        self.client.messages.create(
            from_=f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',
            body=msg,
            to=f'whatsapp:{os.environ["TWILIO_VERIFIED_NUMBER"]}'
        )

        with smtplib.SMTP("smtp.gmail.com") as cnc:
            cnc.starttls()
            cnc.login(self.email, self.pwd)
            for e in list:
                cnc.sendmail(
                    from_addr=self.email,
                    to_addrs=e,
                    msg=f"Subject:New Low Price Flight!\n\n{msg}".encode('utf-8')
                )

