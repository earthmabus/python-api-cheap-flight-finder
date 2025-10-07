import requests
import os

SHEETYCO_BEARER_TOKEN = os.environ.get("SHEETYCO_BEARER_TOKEN")

class DataManager:
    '''
    this class fronts the data source that holds information about users and the trips they're interested in.

    it pulls data from a google sheet.

    the sheet contains two worksheets.
    the "users" sheet contains info about the user (name, username, email address).
    the "prices" sheet contains info about the trips users want to take (destination, price).

    change the underlying data structure into a respectable relational database in the future.
    '''
    def __init__(self):
        # load all users from the "'"users" sheet into self.m_all_users
        self.m_all_users = []
        self.load_all_users_from_sheet()

    #This class is responsible for talking to the Google Sheet.
    def get_data(self):
        '''returns a list of dictionary (city, iataCode, lowestPrice) for the user'''
        headers = { "Authorization": f"Bearer {SHEETYCO_BEARER_TOKEN}" }
        response = requests.get(url="https://api.sheety.co/3a66a46ee7c6d694f1a39c8a7971826a/flightDeals/prices", headers=headers)
        response.raise_for_status()

        # the response will contain this structure...
        # {
        #     "prices": [
        #         {
        #             "city": "Paris",
        #             "iataCode": "",
        #             "lowestPrice": 54,
        #             "id": 2
        #         },
        #         {
        #             "city": "Frankfurt",
        #             "iataCode": "",
        #             "lowestPrice": 42,
        #             "id": 3
        #         },
        #         {
        #             "city": "Tokyo",
        #             "iataCode": "",
        #             "lowestPrice": 485,
        #             "id": 4
        #         }
        #     ]
        # }
        # print(json.dumps(response.json(), indent=4))
        return response.json()['prices']

    def load_all_users_from_sheet(self):
        sheety_headers = { "Authorization": f"Bearer {SHEETYCO_BEARER_TOKEN}" }
        response = requests.get(url="https://api.sheety.co/3a66a46ee7c6d694f1a39c8a7971826a/flightDeals/users", headers=sheety_headers)
        response.raise_for_status()
        self.m_all_users = response.json()['users']

    def get_user_info(self, username):
        '''returns the entry from the "users" sheet for the specified user; returns None if user does not exist'''
        for user in self.m_all_users:
            if username == user['username']:
                return user
        return None

    def get_email_address(self, username):
        '''returns the email address for the specified username; returns None if user does not exist'''
        user = self.get_user_info(username)
        if user is None:
            return None
        return user['email']

    def add_user(self, username, email, firstname, lastname, home_iata_code):
        sheety_header = {"Authorization": f"Bearer {SHEETYCO_BEARER_TOKEN}"}
        sheety_body = {
            "user": {
                "username": username,
                "firstName": firstname,
                "lastName": lastname,
                "email": email,
                "homeIataCode": home_iata_code
            }
        }
        response = requests.post(url="https://api.sheety.co/3a66a46ee7c6d694f1a39c8a7971826a/flightDeals/users", json=sheety_body, headers=sheety_header)
        #print(response.text)
        response.raise_for_status()

        # reload all users from the sheet into memory
        self.load_all_users_from_sheet()

    def add_destination_city(self, username: str, city: str, iata_code: str, lowest_price: float):
        sheety_header = { "Authorization": f"Bearer {SHEETYCO_BEARER_TOKEN}" }
        sheety_body = {
            "price": {
                "city": city,
                "iataCode": iata_code,
                "lowestPrice": lowest_price,
                "username": username
            }
        }
        response = requests.post(url="https://api.sheety.co/3a66a46ee7c6d694f1a39c8a7971826a/flightDeals/prices", json=sheety_body, headers=sheety_header)
        print(response.text)
        response.raise_for_status()
