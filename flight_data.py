import os
from dotenv import load_dotenv
import requests
import time
from typing import Optional

load_dotenv()
AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY')
AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET')

class FlightData:
    """Handles Amadeus API authentication and city code lookups"""
    def __init__(self):
        self._token: Optional[str] = None
        self._token_expiry: Optional[float] = None
        
    def _get_auth_token(self) -> str:
        """Get fresh authentication token"""
        auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": AMADEUS_API_KEY,
            "client_secret": AMADEUS_API_SECRET
        }
        
        try:
            response = requests.post(auth_url, data=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            self._token = data["access_token"]
            self._token_expiry = time.time() + data["expires_in"]
            return self._token
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Authentication failed: {str(e)}")

    def get_city_code(self, city_name: str) -> Optional[str]:
        """Get IATA code for a city name"""
        if not self._token or time.time() > self._token_expiry:
            self._get_auth_token()

        url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        params = {"keyword": city_name, "max": 5}
        headers = {"Authorization": f"Bearer {self._token}"}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            cities = response.json().get("data", [])
            
            for city in cities:
                if city["name"].lower() == city_name.lower():
                    return city["iataCode"].upper()
            return None
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"City lookup failed: {str(e)}")