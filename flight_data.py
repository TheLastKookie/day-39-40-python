class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, price, departure_city_name, departure_iata_code,
                 arrival_city_name, arrival_iata_code, outbound_date, inbound_date, stop_over=0, via_city=""):
        self.price = price
        self.departure_city_name = departure_city_name
        self.departure_iata_code = departure_iata_code
        self.arrival_city_name = arrival_city_name
        self.arrival_iata_code = arrival_iata_code
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date
        self.stop_over = stop_over
        self.via_city = via_city
