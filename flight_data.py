import data_manager as dm
from flight_search import FlightSearch

# Creating the FlightData(FD) class
class FlightData:

    def __init__(self):
        self.cities = []
    # The iata function uses the return of the get_sheet_data function to see if the iata code column is empty
    # If it is, it creates a list and parses that into the search.location function to retrieve them.
    def iata_code_check(self):
        search = FlightSearch()
        sheet_data = dm.get_sheet_data()
        for _ in sheet_data:
            if _[1] == '':
                self.cities.append(_[0])

        iata_codes = search.location_search(self.cities)
        dm.put(iata_codes)
    # Get flying from does the same as above but takes a string input (the departing city)
    def get_flying_from(self, city):
        search = FlightSearch()
        flying_from = search.location_search(city)
        return flying_from
