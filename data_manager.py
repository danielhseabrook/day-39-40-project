import gspread

sa_key = gspread.service_account()
worksheet = sa_key.open("Flight Deals").worksheet("Prices")


def get_sheet_data():

    sheet_data = worksheet.get_all_values()
    del sheet_data[0]
    return sheet_data


def convert_to_dict(data):
    prices = {}
    x = 0
    for _ in data:
        x += 1
        price = {'city': _[0], 'iata_code': _[1], 'max_price': int(_[2])}
        prices[_[0]] = price
    return prices


def put(data_list):
    for _ in data_list:
        cell = 'B' + str(data_list.index(_) + 2)
        print(cell)
        worksheet.update(cell, _)
