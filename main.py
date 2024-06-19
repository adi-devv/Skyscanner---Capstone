import requests, json
from datetime import *
import time
from searchF import FlightSearch
from flight_data import FlightData

# F = FlightData(token="duffel_test_v")
searchF = FlightSearch()

sheet_ep = "https://api.sheety.co/40/flightDeals/prices"
h2 = {
    "Authorization": "Bearer heheeha"
}

sheet_resp = requests.get(sheet_ep, headers=h2)
sheet_data = sheet_resp.json()["prices"]

file = open("Airports.txt", "r+")
airports = json.load(file)

print('runnning')
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for v in sheet_data:
    if v['iataCode'] == '':
        v['iataCode'] = airports.get(v['city'], 'Missing')
        resp = requests.put(
            url=f"{sheet_ep}/{v['id']}",
            json={
                "price": {"iataCode": v["iataCode"]}
            },
            headers=h2
        )
        print(resp.text)

    # ------------------------------------------ PRICE PART ------------------------------------------ #

    flights = searchF.check_flights(
        "DEL",
        v["iataCode"],
        from_time=datetime.now() + timedelta(days=1),
        to_time=datetime.now() + timedelta(days=(6))
    )
    cheapest_flight = FlightData.find_cheapest_flight(flights)
    print(f"{v['city']}: INR {cheapest_flight.price}")
    time.sleep(2)
    break
