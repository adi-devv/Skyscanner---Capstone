import requests, json
from datetime import *
import time
from searchF import FlightSearch
from flight_data import FlightData
from notmgr import notmgr
import os
from dotenv import load_dotenv

load_dotenv()
searchF = FlightSearch()
notmgr = notmgr()

sheet_ep = f"https://api.sheety.co/{os.environ['SHEETY_USERNAME']}/flightDeals/prices"
h2 = {
    "Authorization": f"Bearer {os.environ['SHEETY_PWD']}"
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
        from_time=datetime.now() + timedelta(days=2),
        to_time=datetime.now() + timedelta(days=(6))
    )
    cheapest_flight = FlightData.find_cheapest_flight(flights)
    print(f"{v['city']}: INR {cheapest_flight.price} : {cheapest_flight.out_date} : {cheapest_flight.return_date}")
    time.sleep(2)

    resp = requests.put(
        url=f"{sheet_ep}/{v['id']}",
        json={
            "price": {"lowestPrice": cheapest_flight.price}
        },
        headers=h2
    )

    if cheapest_flight.price != "N/A" and cheapest_flight.price < v["lowestPrice"]:
        print("Lower price found to", v['city'])

        notmgr.whatsapp(
            msg=f"Low price alert! Only £{cheapest_flight.price} to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )
        notmgr.sms(
            msg=f"Low price alert! Only £{cheapest_flight.price} to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )
