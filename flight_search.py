import requests
from flight_data import FlightData
import os

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API = os.environ.get("TEQUILA_API")

DEPARTURE_IATA_CODE = "NYC"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.header = {"apikey": TEQUILA_API}

    def get_iata_code(self, city):
        flight_search_config = {
            "term": city,
            "location_types": "city",
        }

        tequila_response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/locations/query",
            params=flight_search_config,
            headers=self.header
        )
        return tequila_response.json()["locations"][0]["code"]

    def get_flights(self, arrival_city, date_from, date_to, max_stopovers):
        flight_search_config = {
            "fly_from": DEPARTURE_IATA_CODE,
            "fly_to": arrival_city,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "curr": "USD",
            "max_stopovers": max_stopovers,
        }
        flight_search_response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            params=flight_search_config,
            headers=self.header
        )

        try:
            data = flight_search_response.json()["data"][0]
        except IndexError:
            print(f"No flights for {arrival_city}.")
            return None
        else:
            flight_data = FlightData(
                price=data["price"],
                departure_city_name=data["cityFrom"],
                departure_iata_code=data["flyFrom"],
                arrival_city_name=data["cityTo"],
                arrival_iata_code=data["flyTo"],
                outbound_date=data["route"][0]["local_departure"].split("T")[0],
                inbound_date=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.arrival_city_name}: ${flight_data.price}")
            return flight_data
