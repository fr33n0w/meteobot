# LXMF Meteo Bot v1.0 by F. from Reticulum Italia

# DESCRIPTION:                                                                                                                                                             
LXMF Meteo Bot based on the original LXMF Receiver script from markqvist. Weather Data from: Open-Meteo Api                                                                                   
Double script version: meteobot.py (Manual terminal version with user input setup) and meteobot_service.py (to run in systemd passing arguments to the script). 

# BASIC INFORMATION:
You can run the script in manual mode, launching "python meteobot.py" command, and following the on-screen easy setup requests,
or as a system service, using arguments, to avoid user intervention that will cause errors in the systemd.

To run as systemd service use in the service file: "python meteobot_service.py --display_name Bot Name --announce_time 300 --stamp_cost 0" (edit values as you want)
if no argument are passed to the script, it uses default display name: "Meteo Bot - MSG ME!" default announce time of 300 secs , default disabled stamp cost (zero)

Launched from terminal, it will display the LXMF address of the bot, and will show received incoming messages with all relative details.

Note: This bot creates a temporary identity, everytime you close it you will loose the current identity. New launch, new identity. Will be Fixed in future versions.
-

# REQUIREMENTS:
Python modules required: RNS, LXMF, requests, geopy

Install requirements with:
-pip install rns lxmf requests geopy


# INSTALLATION:

Terminal Manual Version:
Download the script meteobot.py from this github release in a folder of your choice.

System Service Version:
Download the script meteobot_service.py from this github release in a folder of your choice.
Create your systemd service file including the necessary arguments (see below...)


# LAUNCH:

- Terminal version: python meteobot.py and follow on-screen instructions.

- Service version with arguments: python meteobot_service.py --display_name YOUR_BOT_NAME --announce_time
  if you don't use arguments, default parameters will be used (default display name: "Meteo Bot - MSG ME!" default announce time of 300 secs , default disabled stamp cost 0)

 (use python or python3 based on your system!)


# Feedback, info and bug reports are welcome, contact me on LXMF address: 0d051f3b6f844380c3e0c5d14e37fac8


# SCREENSHOTS:
coming soon!
 
