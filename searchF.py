import requests
import os
from dotenv import load_dotenv

load_dotenv()

flight_ep = "https://test.api.amadeus.com/v2/shopping/flight-offers"
tok_ep = "https://test.api.amadeus.com/v1/security/oauth2/token"


class FlightSearch:
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=tok_ep, headers=header, data=body)
        return response.json()['access_token']

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "INR",
            "max": "10",
        }

        response = requests.get(url=flight_ep, headers=headers, params=query)
        if response.status_code != 200:
            return None
        if response.json() == None or not response.json()['data']:
            query['nonStop'] = "false"
            response = requests.get(url=flight_ep, headers=headers, params=query)
            if response.status_code != 200:
                return None
        return response.json()
