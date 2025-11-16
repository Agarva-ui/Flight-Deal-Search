from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

from_country = input("where are you now?: ")
to_country = input("where would you like to go?: ")

token = FlightData()._get_auth_token()

orgin_country = FlightData().get_city_code(from_country.lower())
travel_country = FlightData().get_city_code(to_country.lower())

flight = FlightSearch(orgin_code=orgin_country,trave_country_code=travel_country,token=token)
price = flight.get_cheapest_flight()
currency = flight.get_currency()
airLines = flight.get_airline_name()

if price != 0:
    NotificationManager(from_country_code=orgin_country, to_country_code=travel_country, price=price, currency=currency, airlines=airLines)
else:
    print("Could Not Find")


