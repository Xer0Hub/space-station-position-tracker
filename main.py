import time

import requests
from datetime import datetime
import smtplib

MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#ALL FUNCTION DEFINITIONS
def iss_close_to_me():
    leeway = 5
    if abs(MY_LAT - iss_latitude) <= 5 and MY_LONG == iss_longitude <= 5:
        return True
    return False

def timer():
    seconds = 0
    for second in range(4):
        seconds += 1
        time.sleep(1)
        print(seconds)
    if seconds >= 4:
        return seconds

def check_for_iss():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=TARGET, msg="Subject: LOOK UP AND SEE THE ISS!\n\n The ISS is directly overhead, look up now to see it!")
        print("Complete!")
        if timer() == 4:
            print("New message sent!")
            check_for_iss()


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

#GRABS THE CURRENT DATE -> TIME -> HOUR
date_time_now = datetime.now()
time_now = date_time_now.time()
time_hour = time_now.hour

#YOUR CREDENTIALS FOR THE EMAIL AND TARGET
MY_EMAIL = "your_email@gmail.com"
MY_PASSWORD = "your_app_password"
TARGET = "the_person_you_want_to_email"

if iss_close_to_me() and time_hour >= sunset:
    check_for_iss()
else:
    print("ISS isn't close yet")




