import data_manager
import flight_search
import notification_manager
from datetime import datetime, timedelta

# MANAGERS
data_manager = data_manager.DataManager()
flight_search_manager = flight_search.FlightSearch()
notification_manager = notification_manager.NotificationManager()

sheet_data = data_manager.get_sheet_data("prices")

# If the IATA Code column is empty then we fill it in
if sheet_data[0]["iataCode"] == "":
    for city_data in sheet_data:
        city_data["iataCode"] = flight_search_manager.get_iata_code(city=city_data["city"])
        # print(f"sheet_data:\n {sheet_data}")

    data_manager.sheet_data = sheet_data
    data_manager.update_iata_code()

# Find the cheapest flights
today = datetime.now()
tomorrow = today + timedelta(days=1)
six_months = today + timedelta(days=(6 * 30))
for city_data in sheet_data:
    flight_search_data = flight_search_manager.get_flights(
        arrival_city=city_data["iataCode"],
        date_from=tomorrow.strftime("%d/%m/%Y"),
        date_to=six_months.strftime("%d/%m/%Y"),
        max_stopovers=0
    )
    if flight_search_data is None:
        print("TRYING FOR 1 STOP")
        flight_search_data = flight_search_manager.get_flights(
            arrival_city=city_data["iataCode"],
            date_from=tomorrow.strftime("%d/%m/%Y"),
            date_to=six_months.strftime("%d/%m/%Y"),
            max_stopovers=1
        )
    if flight_search_data is not None:
        if flight_search_data.price < city_data["lowestPrice"]:
            notification_manager.send_message(flight_data=flight_search_data)
            user_data = data_manager.get_sheet_data("users")
            notification_manager.send_emails(user_data=user_data)
