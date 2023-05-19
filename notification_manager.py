from twilio.rest import Client
from os import environ as env
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
load_dotenv('/home/dan/pythonProject/envvar.env')


class NotificationManager:
    def __init__(self):
        self.twilio_number = env['TWILIO_NUMBER']
        self.twilio_accsid = env['TWILIO_ACCSID']
        self.twilio_authtoken = env['TWILIO_AUTHTOKEN']
        self.client = Client(self.twilio_accsid, self.twilio_authtoken)
        self.smptp_apikey = env['GMAIL_APIKEY']
        self.my_email = env['MY_EMAIL']
        self.smtp_server = ""

    def send_text_notification(self, data, prices, departing, recipient):
        if 'via_city' not in data:
            self.client.messages.create(
                body=f'DEAL ALERT\nFlight to {data["destination_city"]}, {prices["iata_code"]} from'
                     f' {data["departing_city"]}, {departing} on date/time {data["local_departure"]} for £{data["price"]}',
                from_=self.twilio_number,
                to=recipient
            )
            print(f'DEAL ALERT\nFlight DIRECT to {data["destination_city"]}, {prices["iata_code"]} from'
                  f' {data["departing_city"]}, {departing} on date/time {data["local_departure"]} for £{data["price"]}')
        else:
            print(f'DEAL ALERT\nFlight to {data["destination_city"]}, {prices["iata_code"]} VIA {data["via_city"]} from'
                  f' {data["departing_city"]} {departing} on date/time {data["local_departure"]} for £{data["price"]}')

    def send_email_notification(self, data, prices, departing, recipient):
        with smtplib.SMTP_SSL('smtp.gmail.com', port=465) as connection:
            connection.login(user=self.my_email, password=self.smptp_apikey)
            if 'via_city' not in data:
                msg = (f'Subject: DEAL ALERT -- CHEAP FLIGHT TO {data["destination_city"]}\n\n\n '
                       f'Flight to {data["destination_city"]}, {prices["iata_code"]} '
                       f'from {data["departing_city"]} {departing} on date/time {data["local_departure"]} '
                       f'for £{data["price"]}').encode('utf-8').strip()
                connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=recipient,
                    msg=msg)

            else:
                msg = (f'Subject: DEAL ALERT -- CHEAP FLIGHT TO {data["destination_city"]}\n\n\n '
                       f'Flight to {data["destination_city"]}, {prices["iata_code"]} VIA {data["via_city"]} '
                       f'from {data["departing_city"]} {departing} on date/time {data["local_departure"]} '
                       f'for £{data["price"]}').encode('utf-8').strip()
                connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=recipient,
                    msg=msg)

    def send_notifications(self, data, prices, departing, recipient):
        for _ in recipient:
            if _[0] == '+':
                print('sending text')
                self.send_text_notification(data, prices, departing, recipient)
            else:
                self.send_email_notification(data, prices, departing, recipient)


