import os
import subprocess
import time
import signal
from datetime import datetime
import random
import logging
from threading import Thread, Event
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define your proxy list here
proxy_list = [
    "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678",
    "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631",
    "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445",
    "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928",
    "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128",
    "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080",
    "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800",
    "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678",
    "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820",
    "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080",
    "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016",
    "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542",
    "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153",
    "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145",
    "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145",
    "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145",
    "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137",
    "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128",
    "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678",
    "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145",
    "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080",
    "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145",
    "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145",
    "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334",
    "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145",
    "https://80.78.23.49:1080"
]

# Dictionary to hold user sessions and their assigned proxies
user_proxies = defaultdict(lambda: random.choice(proxy_list))

def update_proxy(user_id):
    proxy = random.choice(proxy_list)
    user_proxies[user_id] = proxy
    logging.info(f"Proxy for user {user_id} updated to {proxy}.")

def periodic_proxy_update(user_id, interval, stop_event):
    while not stop_event.is_set():
        update_proxy(user_id)
        stop_event.wait(interval)

def make_executable():
    try:
        subprocess.run('chmod +x *', shell=True, check=True)
        print("All files in the current directory are now executable.")
    except subprocess.CalledProcessError as e:
        print(f"Error making files executable: {e}")

def log(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] {message}")

def run_bot_script():
    try:
        process = subprocess.Popen(['python3', '/storage/emulated/0/Download/telegram/m10.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log("Bot script started.")
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            log(f"Bot script crashed with error: {stderr.decode()}")
        else:
            log("Bot script exited normally.")
    except Exception as e:
        log(f"An error occurred while running the bot script: {e}")

def signal_handler(sig, frame):
    log(f"Signal {sig} detected. Stopping all processes...")
    cleanup()
    os._exit(0)

def cleanup():
    for user_id, (thread, stop_event) in user_threads.items():
        stop_event.set()
        thread.join()
    log("Cleaned up all user threads.")

if __name__ == "__main__":
    # Initialize the bot
    make_executable()
    log("Bot script starting...")
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the external bot script
    Thread(target=run_bot_script, daemon=True).start()

    # Dictionary to hold threads and stop events for each user
    user_threads = {}

    def start_proxy_update_for_user(user_id):
        if user_id not in user_threads:
            stop_event = Event()
            thread = Thread(target=periodic_proxy_update, args=(user_id, 10, stop_event), daemon=True)
            thread.start()
            user_threads[user_id] = (thread, stop_event)
            log(f"Started proxy update thread for user {user_id}.")

    # Monitor for new users (Simulating user interaction detection)
    while True:
        # Simulate user interaction (Replace with actual user detection logic)
        # e.g., Fetch new users from a queue or database
        new_user_id = random.randint(1, 10000)
        start_proxy_update_for_user(new_user_id)
        time.sleep(1)  # Check for new users every second
