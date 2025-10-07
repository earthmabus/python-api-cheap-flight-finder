import requests
import os

SHEETYCO_BEARER_TOKEN = os.environ.get("SHEETYCO_BEARER_TOKEN")

class DataManager:
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
