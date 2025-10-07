from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import datetime as dt

MY_CITY_CODE = "MCO"
TRIP_DURATION_IN_DAYS = 2
DAY_OF_WEEK_FRIDAY = 4

MAX_NUM_DAYS_LOOKAHEAD = 28 * 6

def is_friday(day: dt.datetime) -> bool:
    '''determines if a specified datetime is a friday (used to search for weekend deals)'''
    return day.weekday() == DAY_OF_WEEK_FRIDAY

# for each city, determine if there are any good prices within the next 2 weeks
def search_for_weekend_deals(flight_search, city_price_list, first_day_of_search, num_of_days_to_lookahead):
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
            matching_flights = flight_search.any_cheap_flights(origin_code=MY_CITY_CODE, dest_code=dest_code, departure_date=date2search_string, return_date=return_date_string, num_adults=2, max_price_to_pay=price_point)

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

    # return none or a dict of { subject, message }
    retval = None
    if len(all_matches) > 0:
        retval = { "subject": subject, "message": message }
    return retval

def search_and_email(data_manager: DataManager):
    # get the current date so we can search for flights between now and next 2 weeks
    current_date = dt.datetime.now()

    # instantiate a DataManager to get travel and price preferences
    dataman = DataManager()
    city_list = data_manager.get_data()

    # instantiate a FlightSearch to search for flight deals
    fs = FlightSearch()
    fs.get_access_token()

    # use the aformentioned objects to search for deals
    all_weekend_matches = search_for_weekend_deals(fs, city_list, current_date, MAX_NUM_DAYS_LOOKAHEAD)

    # construct an email with the weekend deals
    if all_weekend_matches != []:
        print("there are matches -- sending email!")
        email_details = construct_email(all_weekend_matches)
        nm = NotificationManager()
        nm.send_email("earthmabus@hotmail.com", email_details['subject'], email_details['message'])
    else:
        print("sorry, no weekend deals")

def add_new_user(data_manager: DataManager):
    username = input("enter a username for yourself: ")
    email = input("enter your email address: ")
    first_name = input("enter your first name: ")
    last_name = input("enter your last name: ")
    home_iata_code = input("enter your home airport IATA Code: ")

    data_manager.add_user(username, email, first_name, last_name, home_iata_code)
    print(f"successfully created '{username}'")

def add_user_flights(data_manager: DataManager):
    # ensure that the specified user exists before adding an entry
    username = input("enter the username: ")
    if data_manager.get_user_info(username) is None:
        print(f"the specified username '{username}' does not exist; please add the user into the system first")
        print()
        return

    # at this point we know the username exists...
    # collect the information regarding the destination
    city = input("enter the destination city: ")
    city_iata_code = input("enter the IATA code for the city: ")
    lowest_price = float(input("enter the lowest price you're willing to pay for this airfare: "))

    # add the destination into the data_manager
    data_manager.add_destination_city(username, city, city_iata_code, lowest_price)
    print(f"successfully added new tracker to {city_iata_code} at ${lowest_price}")

def menu(data_manager: DataManager):
    print("what would you like to do today?")
    print("1. add a new user")
    print("2. add destination city for user")
    print("3. perform search and email")
    print("4. quit")
    print()
    selection = int(input("what is your selection? "))
    print()

    if selection == 1:
        print("adding new user...")
        add_new_user(data_manager)
    elif selection == 2:
        print("adding city to track flight prices for...")
        add_user_flights(data_manager)
    elif selection == 3:
        print("searching and emailing all users...")
        search_and_email(data_manager)
    elif selection == 4:
        print("exiting program...")
    else:
        print("invalid selection")

# instantiate a DataManager to get travel and price preferences
dataman = DataManager()

menu(dataman)