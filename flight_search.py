import requests
import os
from flight_data import FlightData
import json

AMADEUS_API_KEY = os.environ.get("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.environ.get("AMADEUS_API_SECRET")

class FlightSearch:
    def __init__(self):
        self.m_access_token = self.get_access_token()
        
    def get_access_token(self):
        header = { "Content-Type": "application/x-www-form-urlencoded" }
        body = {
            "grant_type": "client_credentials",
            "client_id": AMADEUS_API_KEY,
            "client_secret": AMADEUS_API_SECRET
        }
        response = requests.post(url="https://test.api.amadeus.com/v1/security/oauth2/token", data=body, headers=header)
        response.raise_for_status()
        return response.json()['access_token']

    def request_flights(self, origin_code, dest_code, departure_date, return_date, num_adults):
        headers = { "Authorization": f"Bearer {self.m_access_token}" }
        params = {
            "originLocationCode": origin_code,
            "destinationLocationCode": dest_code,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": num_adults
        }
        response = requests.get(url="https://test.api.amadeus.com/v2/shopping/flight-offers", params=params, headers=headers)
        response.raise_for_status()
        # if response.status_code == 200:
        #     # success
        # elif response.status_code == 425:
        #     # invalid date
        # elif response.status_code == 477:
        #     # invalid format
        # elif response.status_code == 2668:
        #     # parameter combination invalid/restricted
        # elif response.status_code == 4926:
        #     # invalid data received
        # elif response.status_code == 10661:
        #     # maximum number of occurrences exceeded
        # elif response.status_code == 32171:
        #     # mandatory data missing
        #print(f"json: {json.dumps(response.json(), indent=4)}")
        #print(f"\n\n\n{response.json()}")
        return response.json()

    def any_cheap_flights(self, origin_code, dest_code, departure_date, return_date, num_adults, max_price_to_pay: float):
        matching_flights = []
        flights = self.request_flights(origin_code, dest_code, departure_date, return_date, num_adults)
        #print(f"there are {len(flights['data'])} flights")
        for flight in flights['data']:
            # for itinerary in flight['itineraries']:
            #     print(f"- there are {len(flight['itineraries'])} itineraries with {len(itinerary['segments'])} segments")
            #     for segment in itinerary['segments']:
            #         print(f"  - carrier: {segment['carrierCode']}, number: {segment['number']}, num of stops: {segment['numberOfStops']}")
            #         print(f"  - segment: departure: {segment['departure']['iataCode']} --> arrival: {segment['arrival']['iataCode']}")
            # print(f"  - price: {flight['price']['grandTotal']}")
            if float(flight['price']['grandTotal']) <= max_price_to_pay:
                matching_flights.append(FlightData(flight))

        #print(f"there were {len(flights['data'])} flights for {origin_code} to {dest_code} on {departure_date}, but only {len(matching_flights)} were {max_price_to_pay} or less")
        return matching_flights
