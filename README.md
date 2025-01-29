# Slasher
Im tired of python malware being lame.

- Slasher is a 3-Stage Attack Remote Access Trojan written in Python. 

- It is designed to be self-sufficient and doesnt depend on the target's python installation being set up properly, solving the most annoying and unpredicatble part of python malware developement.

- The target only needs python installed on their system for the first run. After that first run slasher makes itself self-sufficient and persists through restarts. 

- It will even continue running if the user uninstalls their python environment!

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

- **More Features Coming Soon!**

# Usage

*if you dont know anything about python, it may be difficult to get slasher running*

1. Set the "TOKEN" variable at the top of payload.py to you your discord bot token.

2. In payload.py, find the variable "id" on line 102 and replace "discord_server_id" with the ID of the server you want the bot to message in.

3. Obfuscate payload.py to avoid AV detections and your bot token being found. (I use [Pyobfuscate](https://pyobfuscate.com))

4. Put embed.py, payload.py, run.vbs and runner.bat in a zip and upload it to some website to download later. (Private github repo is easiest)
   
5. In dropper.py, set the "url" variable on line 24 to the download link to your zip file.

6. Obfuscate dropper.py or bundle it with another program! Anybody who runs it will be infected!

# How It Works
Slasher is a three-stage attack comprised of 5 files. Below is a description of each file's functionality in order of execution.


## *dropper.py*

dropper.py is the first file in the attack chain. It is meant to be compatible with as many python versions as possible, and very easy to bundle into other scripts. 

Functionality
1.  dropper.py starts by installing the modules it needs to the same python installation it was ran from.
   
2.  It downloads and extracts a file, runtime.zip to "C:\Users\your_username\AppData\Roaming\Microsoft\Network\runtime". The downloaded folder contains the rest of the files necessary for the infection.
   
3.  Once the download is complete, it creates a shortcut to run.vbs named runcut.lnk, then adds the shortcut's path to the "Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" Registry key to establish 
    persistance as early as possible.
  
4.  Finally, the file cd's to the runtime folder and runs embed.py using the same python installation that was used to run the dropper.


## *embed.py*

embed.py is the second file in the chain, it works as a middleman to ensure the payload's environement is set up correctly before it is ran. It downloads and sets up a python environment that the target doesnt know about, so slasher cannot be removed from the target device by simply uninstalling python.

Functionality
1. When the file is first ran, it checks for the folder "C:\Users\your_username\AppData\Local\Python398", which is where the dedicated python environment is set up.
   
2. If the folder IS NOT present, the python environment is downloaded and extracted to the folder, then all of the modules necessary for the payload to run are installed.
   
3. If the Folder IS present, it will simply call payload.py using the dedicated python interpreter & environement.


## *payload.py*

payload.py is the payload in the form of a discord bot that runs on the users machine, executing built-in modules via commands, or allowing you to do whatever you want via a live terminal through the discord channel.

Not much else to say here.


# First Run
On the First run, the payload runs directly when embed.py calls it with a sys.executable subprocess. This is to avoid issues with conflicting python installations, and may be changed in the future.
A registry key is set to point to run.vbs on startup. 



# Persistance After System Restart

## *runner.bat*

runner.bat acts as a middleman between run.vbs and the payload execution. It checks if the dedicated environment is set up and determines if payload.py or embed.py should be run. 

If the environement's path DOES exist, it assumes it is set up properly and calls payload.py directly with the dedicated python 3.9.8 executable that was downloaded.

If the environments path DOES NOT exist, it will check environment variables for a python installtion to run embed.py with, and install the dedicated environment. If the dropper executed properly, this should never happen. It is just a failsafe.

This is helpful to ensure the malware continues functioning on the target system long-term.

## *run.vbs*

When the user starts their pc, run.vbs is called, which creates a completely silent, no-window shell and runs runner.bat. It will also loop in the background to ensure payload.py is always running. If it doesnt find it in the process list, it will call runner.bat again.

This file is crucial to the attack chain, as it allows us to run our python files fully in-the-background without the user knowing. 

Adding the keep-alive functionality to this file is helpful because it appears in task manager as "Windows Based Script Host" while the payload will appear as "Python", which is suspicious. Even if the user kills the suspicious python task, it will keep restarting unless they kill the VBS script, which is much much harder for the average user to identify, and looks far less suspicious
