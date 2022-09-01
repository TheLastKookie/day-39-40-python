import requests
import os

SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")
TOKEN = os.environ.get("TOKEN")


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheet_data = {}
        self.sheet_headers = {
            "Authorization": f"Bearer {TOKEN}"
        }

    def get_sheet_data(self, sheet_name):
        sheet_response = requests.get(url=f"{SHEET_ENDPOINT}/{sheet_name}", headers=self.sheet_headers)
        self.sheet_data = sheet_response.json()[sheet_name]
        return self.sheet_data

    def update_iata_code(self):
        for city in self.sheet_data:
            sheet_config = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            sheet_response = requests.put(
                url=SHEET_ENDPOINT + f"/{city['id']}",
                json=sheet_config,
                headers=self.sheet_headers
            )
            print(sheet_response.text)
