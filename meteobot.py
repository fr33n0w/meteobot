####################################################################################################################################################################
## LXMF Meteo Bot v1.0 by F, from Reticulum Italia / Weather Data from: Open-Meteo Api / Official Github: https://github.com/fr33n0w/meteobot                     ##
##                                                                                                                                                                ##
## Simple LXMF Meteo Bot based on the original LXMF Receiver script from markqvist.                                                                               ##
##                                                                                                                                                                ##
## Double script version: meteobot.py (Manual version with user input setup) and meteobot_service.py (to run in systemd passing arguments to the script).         ##
## You can run the script in manual mode, launching "python meteobot.py" command and following the on-screen easy setup requests,                                 ##
## or as a system service, using arguments, to avoid user intervention that will cause errors in the systemd.                                                     ##
##                                                                                                                                                                ##
## To run as systemd service use: "python meteobot_service.py --display_name BotName --announce_time 300 --stamp_cost 0" (edit values as you want)                ##
## if no argument are passed, use default display name: "Meteo Bot - MSG ME!" default announce time of 300 secs , default disabled stamp cost (zero)              ##
##                                                                                                                                                                ##
## Launched from terminal, it will display the LXMF address of the bot, and will show received incoming messages with all relative details.                       ##
##                                                                                                                                                                ##
## Note: This bot creates a temporary identity, everytime you close it you will loose the current identity. New run, new identity. Will be Fixed in next versions.##
##                                                                                                                                                                ##
####################################################################################################################################################################

import RNS
import LXMF
import time
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
from datetime import datetime

# Intro Screen
print("" + "\n")
print("=" * 80)
print(" " * 18 + " >> Welcome to LXMF Meteo Bot v1.0 by F. <<")
print("=" * 80 + "\n")
print(" " * 8 + "This bot retrieves weather information using the Open-Meteo API.")
print(" " * 10 + "The Bot Identity Peer will be reachable in all LXMF clients.\n")
print(" You can customize the display name for the bot and the automatic announce time.")
print(" Set STAMP COST from 1 to 256 for incoming message cost, set to 0 for no stamp cost\n")
print(" " * 18 + "LXMF address will be shown after this intro.\n")
print(" " * 11 + ">> Follow on-screen instruction for easy configuration. <<\n")
print("=" * 80 + "\n")

# Prompt the user to press Enter to continue or Ctrl + C to exit
try:
    input("Press Enter to continue the Setup or Ctrl + C to exit...\n\n")
except KeyboardInterrupt:
    print("\n\n" + "=" * 80)
    print(" " * 14 + ">> Exiting LXMF Meteo Bot v1.0 by F. - Goodbye! <<")
    print("=" * 80)
    exit()

# START GUIDED CONFIGURATION

# SET DISPLAY NAME

try:
    display_name = input("Enter a display name for the bot (or press Enter to use the default 'Meteo Bot - MSG ME!'): ")
    if not display_name.strip():
        display_name = "Meteo Bot - MSG ME!"  # Default display name
except KeyboardInterrupt:
    print("\n" + "=" * 80)
    print(" " * 14 + ">> Exiting LXMF Meteo Bot v1.0 by F. - Goodbye! <<")
    print("=" * 80)
    exit()

# SET AUTO-ANNOUNCE TIME IN SECONDS
while True:
    try:
        announce_time = int(input("Enter the announce time in seconds (default is 300 seconds): ") or 300)
        if announce_time <= 0:
            print("Please enter a positive integer.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

# SET STAMP COST
while True:
    try:
        stamp_cost = int(input("Enter the stamp cost value (1 to 256 to enable, 0 to disable): ") or 0)
        if stamp_cost < 0 or stamp_cost > 256:
            print("Please enter a value between 0 and 256.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")


required_stamp_cost = stamp_cost
enforce_stamps = False

geolocator = Nominatim(user_agent="my_geopy_app")

# Mapping of weather codes to descriptions
weather_code_mapping = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light",
    53: "Drizzle: Moderate",
    55: "Drizzle: Heavy",
    61: "Rain: Light",
    63: "Rain: Moderate",
    65: "Rain: Heavy",
    71: "Snow fall: Light",
    73: "Snow fall: Moderate",
    75: "Snow fall: Heavy",
    80: "Rain showers: Light",
    81: "Rain showers: Moderate",
    82: "Rain showers: Heavy",
    95: "Thunderstorm: Light",
    96: "Thunderstorm: Heavy",
    99: "Thunderstorm with hail",
    # Full weather codes
    100: "Clear sky",
    101: "Mainly clear",
    102: "Partly cloudy",
    103: "Overcast",
    104: "Fog",
    105: "Depositing rime fog",
    106: "Drizzle: Light",
    107: "Drizzle: Moderate",
    108: "Drizzle: Heavy",
    109: "Rain: Light",
    110: "Rain: Moderate",
    111: "Rain: Heavy",
    112: "Snow fall: Light",
    113: "Snow fall: Moderate",
    114: "Snow fall: Heavy",
    115: "Rain showers: Light",
    116: "Rain showers: Moderate",
    117: "Rain showers: Heavy",
    118: "Thunderstorm: Light",
    119: "Thunderstorm: Heavy",
    120: "Thunderstorm with hail"
}

def get_weather(latitude, longitude):
    # OpenMeteo API endpoint for weather data
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        weather_data = response.json()
        
        current_weather = weather_data.get("current_weather", {})
        if current_weather:
            current_temperature = current_weather.get('temperature')
            current_humidity = current_weather.get('relativehumidity', "N/A")
            current_windspeed = current_weather.get('windspeed')
            current_winddirection = current_weather.get('winddirection')
            current_weathercode = current_weather.get('weathercode')
            current_timestamp = datetime.now()

            # Get the weather description from the mapping
            current_weather_description = weather_code_mapping.get(current_weathercode, "Unknown weather code")

            daily_forecast = weather_data.get("daily", {})
            daily_max_temperature = daily_forecast.get("temperature_2m_max", [])
            daily_min_temperature = daily_forecast.get("temperature_2m_min", [])
            daily_precipitation = daily_forecast.get("precipitation_sum", [])

            weather_info = f"""{current_timestamp}
            -------------------------------------

            >> Current Weather:
            Temperature: {current_temperature}°C
            Humidity: {current_humidity}%
            Wind Speed: {current_windspeed} km/h
            Wind Direction: {current_winddirection}°
            Weather Status: {current_weather_description}
                           
            >> Daily Forecast:
            Max Temperatures: {daily_max_temperature}
            Min Temperatures: {daily_min_temperature}
            Precipitation: {daily_precipitation}
            ----------------------------------------------------------
            >>    Weather Data from Open-Meteo API    <<
            ----------------------------------------------------------
            Get your Meteo Bot: github.com/fr33n0w/meteobot
            """
            return weather_info
        else:
            return "Weather data not available."
    except requests.RequestException as e:
        return f"Error fetching weather data: {e}"

def delivery_callback(message):
    global my_lxmf_destination, router
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(message.timestamp))
    signature_string = "Signature is invalid, reason undetermined"
    if message.signature_validated:
        signature_string = "Validated"
    else:
        if message.unverified_reason == LXMF.LXMessage.SIGNATURE_INVALID:
            signature_string = "Invalid signature"
        if message.unverified_reason == LXMF.LXMessage.SOURCE_UNKNOWN:
            signature_string = "Cannot verify, source is unknown"

    if message.stamp_valid:
        stamp_string = "Validated"
    else:
        stamp_string = "Invalid"

    print("\t+--- INCOMING REQUEST: ---------------------------------------------")
    print("\t| Source hash            : " + RNS.prettyhexrep(message.source_hash))
    print("\t| Source instance        : " + str(message.get_source()))
    print("\t| Destination hash       : " + RNS.prettyhexrep(message.destination_hash))
    print("\t| Destination instance   : " + str(message.get_destination()))
    print("\t| Transport Encryption   : " + str(message.transport_encryption))
    print("\t| Timestamp              : " + time_string)
    print("\t| Content                : " + str(message.content_as_string()))
    print("\t| Fields                 : " + str(message.fields))
    if message.ratchet_id:
        print("\t| Ratchet                : " + str(RNS.Identity._get_ratchet_id(message.ratchet_id)))
    print("\t| Message signature      : " + signature_string)
    print("\t| Stamp                  : " + stamp_string)
    print("\t+-------------------------------------------------------------------")

    # Process the message content
    content = message.content_as_string()
    if content.startswith("meteo "):
        city_name = content[6:]  # Extract city name
        try:
            location = geolocator.geocode(city_name)
            if location:
                # Get weather information using OpenMeteo
                weather_info = get_weather(location.latitude, location.longitude)
                response_message = f"""
            Meteo Report for {city_name}:
            -------------------------------------
            GPS Position: 
            Latitude: {location.latitude} 
            Longitude: {location.longitude}. 
            -------------------------------------
            {weather_info}
            """
            else:
                response_message = "City not found. Please try another name."
        except GeocoderServiceError as e:
            response_message = f"Error occurred: {e}"
    else:
        response_message = """
        >>  Welcome To Meteo Bot - Get Global Weather Info!  <<
        ------------------------------------------------------------------

        LXMF Meteo Bot v1.0 by F. / Weather from Open-Meteo Api
        
        -------------------------------------------------------------------
        Command usage: \"meteo city name\" - Example: meteo Roma
        """
    
    # Send the response
    source = my_lxmf_destination
    dest = message.source
    lxm = LXMF.LXMessage(dest, source, response_message, None, desired_method=LXMF.LXMessage.DIRECT, include_ticket=True)
    router.handle_outbound(lxm)

# Initialize Reticulum Network Protocola
r = RNS.Reticulum()

# Initialize LXMF Protocol
router = LXMF.LXMRouter(storagepath="./tmp1", enforce_stamps=enforce_stamps)
identity = RNS.Identity()
my_lxmf_destination = router.register_delivery_identity(identity, display_name=display_name, stamp_cost=required_stamp_cost) ## <<< CUSTOMIZE DISPLAY NAME HERE
router.register_delivery_callback(delivery_callback)

# Print LXMF Meteo Bot Address
print("\n" + "=" * 60)
print("METEO BOT LXMF ADDRESS: " + RNS.prettyhexrep(my_lxmf_destination.hash))
print("=" * 60)
input("\nPress Enter to continue...\n\n")

# Announce at the start
print("=" * 60)
print("\n- Announcing Meteo Bot Name and LXMF Address...")
router.announce(my_lxmf_destination.hash)
print("\n>> Meteo Bot Announce Sent!\n")
print("=" * 60)


try:
    while True:
        time.sleep(announce_time)  # Use the user-defined announce time
        print("=" * 60)
        print("\n- Auto-Announcing Meteo Bot Name and LXMF Address...")
        router.announce(my_lxmf_destination.hash)
        print("\n>> Meteo Bot Announce Sent!\n")
        print("=" * 60)
except KeyboardInterrupt:
    print("=" * 80)
    print(" " * 14 + ">> Exiting LXMF Meteo Bot v1.0 by F. - Goodbye! <<")
    print("=" * 80)
    exit()