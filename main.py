from data_manager import DataManager
from flight_search import FlightSearch
import datetime as dt

MY_CITY_CODE = "MCO"
TRIP_DURATION_IN_DAYS = 2
DAY_OF_WEEK_FRIDAY = 4

MAX_NUM_DAYS_LOOKAHEAD = 28 * 4

def is_friday(day: dt.datetime) ->bool:
    '''determines if a specified datetime is a friday (used to search for weekend deals)'''
    return day.weekday() == DAY_OF_WEEK_FRIDAY

# for each city, determine if there are any good prices within the next 2 weeks
def search_for_weekend_deals(city_price_list, first_day_of_search, num_of_days_to_lookahead):
    retval = []
    for city in city_price_list:
        # get information about the city
        dest_city = city['city']
        dest_code = city['iataCode']
        price_point = city['lowestPrice']

        # examine between start date and end date for flights that match pricing criteria
        for i in range(0, num_of_days_to_lookahead):
            date2search = first_day_of_search + dt.timedelta(days=i)
            date2search_string = date2search.strftime("%Y-%m-%d")
            if not is_friday(date2search):
                continue

            # search for a sunday return flight
            return_date = date2search + dt.timedelta(days=TRIP_DURATION_IN_DAYS)
            return_date_string = return_date.strftime("%Y-%m-%d")

            # look for all cheap flights between my city and the destination
            # print(f"searching for flights on {date2search_string} since it's a friday with return date of {return_date_string}")
            matching_flights = fs.any_cheap_flights(origin_code=MY_CITY_CODE, dest_code=dest_code, departure_date=date2search_string, return_date=return_date_string, num_adults=2, max_price_to_pay=price_point)

            # if there are cheap flights, add it to the comprehensive list of all matches
            [retval.append(flight) for flight in matching_flights]
            # print(f"there were {len(matching_flights)} matching flights for {MY_CITY_CODE} to {dest_code} between {date2search_string} to {return_date_string}")

        return retval

def construct_email(all_matches):
    '''sends out an email with all the flights that matched the pricing criteria'''
    subject=f"There are {len(all_matches)} low price alert(s) from {MY_CITY_CODE} to your destinations!"
    message=""
    for trip in all_matches:
        message += f"${trip.get_total_price()} for {trip.get_departure_iata_code()} to {trip.get_return_iata_code()} between {trip.get_departure_date()} and {trip.get_return_date()}\n"

        # add the departing segments
        depart_segments = trip.get_departure_segments()
        message += f"There are {len(depart_segments)} departing segments:\n"
        for seg in depart_segments:
            message += f"- {seg['carrierCode']} {seg['number']}: {seg['departure']['iataCode']} ({seg['departure']['at'].replace("T", " ")}) -> {seg['arrival']['iataCode']} ({seg['arrival']['at'].replace("T", " ")})\n"

        # add the returning segments
        return_segments = trip.get_return_segments()
        message += f"There are {len(return_segments)} returning segments:\n"
        for seg in return_segments:
            message += f"- {seg['carrierCode']} {seg['number']}: {seg['departure']['iataCode']} ({seg['departure']['at'].replace("T", " ")}) -> {seg['arrival']['iataCode']} ({seg['arrival']['at'].replace("T", " ")})\n"

        message += "\n"

    if len(all_matches) > 0:
        print()
        print(f"Subject: {subject}")
        print(f"Message:\n{message}")
    else:
        print("there are no weekend deals for the specified time ranges")

# get the current date so we can search for flights between now and next 2 weeks
current_date = dt.datetime.now()

# instantiate a DataManager to get travel and price preferences
dataman = DataManager()
city_list = dataman.get_data()

# instantiate a FlightSearch to search for flight deals
fs = FlightSearch()
fs.get_access_token()

# use the aformentioned objects to search for deals
all_weekend_matches = search_for_weekend_deals(city_list, current_date, MAX_NUM_DAYS_LOOKAHEAD)

# construct an email with the weekend deals
construct_email(all_weekend_matches)
