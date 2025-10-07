import json

class FlightData:
    def __init__(self, flight_data):
        self.m_flight_data = flight_data

    def get_number_of_departure_segments(self) -> int:
        return len(self.m_flight_data['itineraries'][0]['segments'])

    def get_number_of_return_segments(self) -> int:
        return len(self.m_flight_data['itineraries'][1]['segments'])

    def get_departure_iata_code(self):
        return self.m_flight_data['itineraries'][0]['segments'][0]['departure']['iataCode']

    def get_return_iata_code(self):
        return self.m_flight_data['itineraries'][1]['segments'][0]['departure']['iataCode']

    def get_departure_date(self) -> str:
        return self.m_flight_data['itineraries'][0]['segments'][0]['departure']['at']

    def get_return_date(self):
        return self.m_flight_data['itineraries'][1]['segments'][0]['departure']['at']

    def get_departure_segments(self):
        return self.m_flight_data['itineraries'][0]['segments']

    def get_return_segments(self):
        return self.m_flight_data['itineraries'][1]['segments']

    def get_total_price(self):
        return self.m_flight_data['price']['grandTotal']

    def print(self):
        print(json.dumps(self.m_flight_data, indent=4))