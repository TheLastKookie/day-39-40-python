from twilio.rest import Client
import smtplib
import os

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH = os.environ.get("TWILIO_AUTH")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")
TO_PHONE = os.environ.get("TO_PHONE")

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.message = ""

    def send_message(self, flight_data):
        client = Client(TWILIO_SID, TWILIO_AUTH)
        self.message = f"Low price alert! Only ${flight_data.price} to fly from " \
               f"{flight_data.departure_city_name}-{flight_data.departure_iata_code} to " \
               f"{flight_data.arrival_city_name}-{flight_data.arrival_iata_code} from " \
               f"{flight_data.outbound_date} to {flight_data.inbound_date}."
        if flight_data.stop_over > 0:
            self.message += f"\nFlight has {flight_data.stop_over} via {flight_data.via_city}."
        message = client.messages.create(
            body=self.message,
            from_=TWILIO_PHONE,
            to=TO_PHONE
        )
        print(message.status)

    def send_emails(self, user_data):
        for user in user_data:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=user["email"],
                    msg=f"Subject:Flight Deal Finder Club\n\n{self.message}"
                )
