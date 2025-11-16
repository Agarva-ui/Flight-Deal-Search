import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self, orgin_code, trave_country_code, token):
        self.headers = {"Authorization": f"Bearer {token}"}
        self.data = {
            'grant_type': 'client_credentials',
            'client_id': API_KEY,
            'client_secret': API_SECRET
        }
        self.params= {
            "originLocationCode" : f"{orgin_code}",
            "destinationLocationCode" : f"{trave_country_code}",
            "departureDate" : datetime.now().strftime("%Y-%m-%d"),
            "adults" : 1

        }
        self.response = requests.get(url="https://test.api.amadeus.com/v2/shopping/flight-offers",params= self.params,headers= self.headers)
        self.result = self.response.json()

    def get_cheapest_flight(self, for_func=0):
        # Find the cheapest flight offer
        self.cheapest_flight = self.result["data"][0]  # default
        cheapest_price = float(self.cheapest_flight["price"]["grandTotal"])
        
        for offer in self.result["data"]:
            price = float(offer["price"]["grandTotal"])
            if price < cheapest_price:
                self.cheapest_flight = offer
                cheapest_price = price
            
        return cheapest_price

    def get_airline_name(self):
        if not hasattr(self, "cheapest_flight"):
            self.get_cheapest_flight()  # make sure we have the cheapest flight
        
        carriers_dict = self.result["dictionaries"]["carriers"]
        airlines = []

        for itinerary in self.cheapest_flight["itineraries"]:
            for segment in itinerary["segments"]:
                code = segment["carrierCode"]  # marketing airline
                name = carriers_dict.get(code, "Unknown Airline")
                airlines.append(name)

        # Remove duplicates if needed
        unique_airlines = list(dict.fromkeys(airlines))
        return unique_airlines

    def get_currency(self):
         self.cheapest_currency = self.result["data"][0]["price"]["currency"]
         return self.cheapest_currency
            
