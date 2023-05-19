from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
import data_manager as dm
from os import environ as env
from dotenv import load_dotenv
load_dotenv('/home/dan/pythonProject/envvar.env')
# Classes
nm = NotificationManager()
fd = FlightData()
fs = FlightSearch()
# Variables
departing = 'Sydney'
destinations = []
currency = 'GBP'
deals = {}
contact_list = []


# Checking if the spreadsheet cities have IATA codes, retrieving if not
fd.iata_code_check()
# Collating IATA codes from spreadsheet into a list

for _ in dm.get_sheet_data():
    destinations.append(_[1])
# Converting spreadsheet data to dict for flight search comparison
price_dict = dm.convert_to_dict(dm.get_sheet_data())
# Retrieving the IATA code for the departing location
departing_code = fd.get_flying_from(departing)
# Inputting the departing code, destination list and currency into the flight search function
flights = fs.check_flights(departing_code, destinations, currency)
# Comparing the maxing price in spreadsheet data to the ticket cost price from the flight search result. Creating a
# new dict 'deals' for the results.
for _ in flights:
    if flights[_]['price'] < price_dict[_]['max_price']:
        deals[_] = flights[_]
# sending SMS notifications with details of the flights in the deals list.
for _ in deals:
    nm.send_notifications(deals[_], price_dict[_], departing_code, dm.get_contact_data())
