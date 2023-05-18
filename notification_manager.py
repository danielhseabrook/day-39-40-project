from twilio.rest import Client
from os import environ as env
from dotenv import load_dotenv
load_dotenv('/home/dan/pythonProject/envvar.env')


class NotificationManager:
    def __init__(self):
        self.twilio_number = env['TWILIO_NUMBER']
        self.twilio_accsid = env['TWILIO_ACCSID']
        self.twilio_authtoken = env['TWILIO_AUTHTOKEN']
        self.my_number = env['MY_NUMBER']
        self.client = Client(self.twilio_accsid, self.twilio_authtoken)

    def send_notification(self, data, prices, departing):
        self.client.messages.create(
            body=f'DEAL ALERT\nFlight to {data["destination_city"]}, {prices["iata_code"]} from'
                 f' {data["departing_city"]}, {departing} on date/time {data["local_departure"]} for £{data["price"]}',
            from_=self.twilio_number,
            to=self.my_number
        )
        print(f'DEAL ALERT\nFlight to {data["destination_city"]}, {prices["iata_code"]} from'
              f' {data["departing_city"]}, {departing} on date/time {data["local_departure"]} for £{data["price"]}')
