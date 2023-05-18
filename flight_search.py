import requests
from datetime import date, timedelta
from os import environ as env
from dotenv import load_dotenv
load_dotenv('/home/dan/pythonProject/envvar.env')


class FlightSearch:
    def __init__(self):
        self.flying_from = ""
        self.start_search_date = date.today() + timedelta(weeks=1)
        self.start_search_date = self.start_search_date.strftime('%d/%m/%Y')
        self.end_search_date = date.today() + timedelta(weeks=26)
        self.end_search_date = self.end_search_date.strftime('%d/%m/%Y')
        self.KIWI_URL = 'https://api.tequila.kiwi.com'
        self.SEARCH_URL = 'https://api.tequila.kiwi.com/v2/search?'
        self.header = {
            'apikey': env['KIWI_SEARCH_APIKEY']
        }

    def location_search(self, data_list):
        if isinstance(data_list, list):
            city_codes = []
            for _ in data_list:
                data = {
                    'term': _
                }
                request = requests.get(url=f'{self.KIWI_URL}/locations/query', headers=self.header, params=data)
                request.raise_for_status()
                city_code = request.json()['locations'][0]['code']
                city_codes.append(city_code)
            return city_codes
        else:
            data = {
                'term': data_list
            }
            request = requests.get(url=f'{self.KIWI_URL}/locations/query', headers=self.header, params=data)
            request.raise_for_status()
            city_code = request.json()['locations'][0]['code']
            return city_code

    def check_flights(self, departing, destination, currency):
        data = []
        flights = {}
        for _ in destination:
            parameters = {
                'fly_from': departing,
                'fly_to': _,
                'date_from': self.start_search_date,
                'date_to': self.end_search_date,
                'curr': currency,
                'max_stopovers': 0,
                'ret_to_diff_airport': 0,
                'return_to_diff_city': False,
                'one_for_city': 1,
                'nights_in_dst_from': 7,
                'nights_in_dst_to': 28,
            }

            response = requests.get(url='https://api.tequila.kiwi.com/v2/search', headers=self.header, params=parameters)
            print(response.status_code)
            response = response.json()
            if len(response['data']) > 0:
                data.append(response['data'])

        for _ in data:
            flight = {
                  'country': _[0]['countryTo']['name'],
                  'departing_city': _[0]['cityFrom'],
                  'destination_city': _[0]['cityTo'],
                  'local_departure': _[0]['local_departure'],
                  'price': _[0]['price']
                  }
            flights[_[0]['cityTo']] = flight

        return flights
