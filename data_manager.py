import gspread
from os import environ as env
from dotenv import load_dotenv

load_dotenv('/home/dan/pythonProject/envvar.env')
sa_key = gspread.service_account()
worksheet = sa_key.open("Flight Deals").worksheet("Prices")
contact_sheet = sa_key.open("Flight Deals").worksheet("customers")
sms_contacts = [env['MY_NUMBER']]


def get_sheet_data():

    sheet_data = worksheet.get_all_values()
    del sheet_data[0]
    return sheet_data


def get_contact_data():
    contacts = contact_sheet.col_values(3)
    del contacts[0]
    contacts += sms_contacts
    return contacts


def convert_to_dict(data):
    prices = {}
    for _ in data:
        try:
            price = {'city': _[0], 'iata_code': _[1], 'max_price': int(_[2])}
            prices[_[0]] = price
        except ValueError:
            print(f"There is an error in the follow record:\n{[_]}\nSkipping. Amend the issue in the Flight Deals"
                  f" spreadsheet to resume checking this location for deals.")

    return prices


def put(data_list):
    for _ in data_list:
        cell = 'B' + str(data_list.index(_) + 2)
        print(cell)
        worksheet.update(cell, _)
