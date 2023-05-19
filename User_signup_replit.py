import gspread
import ast
from os import environ as env
import pandas as pd

credentials = ast.literal_eval(env['credentials2'])

gc = gspread.service_account_from_dict(credentials)
worksheet = gc.open("Flight Deals").worksheet("customers")
data = worksheet.get_all_records()

data.append({
    'First Name': input(
        "Welcome to Flight Co. I love you\nFlight Co., now with more deals.\nJoin the cult\nWhat is your first name?\n"),

    'Last Name': input("What is your last name?\n"),

    'Email': input("What is your email address?\n"),
})

df = pd.DataFrame(data)

worksheet.update([df.columns.values.tolist()] + df.values.tolist())
