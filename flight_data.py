# class FlightData:
#     def __init__(self, token):
#         self.headers = {
#             "Authorization": f"Bearer {token}",
#             "Duffel-Version": "v1",
#             "Content-Type": "application/json",
#         }
#         self.token = token
#
#     def get_airports(self):
#         airports, url = {}, "https://api.duffel.com/air/airports?limit=200"
#         while url:
#             data = requests.get(url, headers=self.headers).json()
#             airports.update({i['city_name']: i['iata_city_code'] for i in data['data']})
#             url = data['meta'].get('after') and f"{url}&after={data['meta']['after']}"
#
#         return {part.strip(): iata_code for city_name, iata_code in airports.items()
#                 for part in (city_name.split('/') if city_name and '/' in city_name else [city_name])}
#
#     def local_save(self):
#         with open("Airports.txt", "w") as file:
#             json.dump(self.airports, file, indent=4)

class FlightData:
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

    def find_cheapest_flight(data):
        if data is None or not data['data']:
            return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

        first_flight = data['data'][0]
        lowest_price = float(first_flight["price"]["grandTotal"])
        origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
        out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
        return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

        cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

        for flight in data["data"]:
            price = float(flight["price"]["grandTotal"])
            if price < lowest_price:
                lowest_price = price
                origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
                out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
                return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
                cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

        return cheapest_flight
