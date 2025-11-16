import smtplib
from datetime import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()

MY_EMAIL = os.getenv('MY_EMAIL')
PASSWORD = os.getenv('PASSWORD')

NOW = dt.now()
FORMATTED_NOW = NOW.strftime("%Y-%m-%d")
class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self,from_country_code,to_country_code,price,currency,airlines) -> None:
        self.after_6_months = int(NOW.month)
        if self.after_6_months >12 :
            self.after_6_months -= 12
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr= MY_EMAIL,
                to_addrs= "anwar.badiea@gmail.com",
                msg=f"Subject: Low Price Alert!!\n\n Only {price} {currency} to fly from {from_country_code} to {to_country_code}, on {FORMATTED_NOW} until {NOW.year}-{self.after_6_months}-{NOW.day}, in these airlines: {", ".join(airlines)}"
            )