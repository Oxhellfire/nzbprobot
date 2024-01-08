from pyrogram import Client
from os import path, environ
from datetime import datetime
from dotenv import load_dotenv


load_dotenv("config.env")

log_file = "nzbprologs.txt"
if path.exists(log_file):
    with open(log_file, 'w') as f:
        pass


class NzbProLogs:
    def __init__(self):
        self.log_file = "nzbprologs.txt"
        self.current_datetime = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

    def info(self, info_message):
        print(f"[+]: {info_message}")
        with open(self.log_file, "a") as f:
            f.write(f"[INFO]({self.current_datetime}): {info_message}\n")

    def error(self, error_message):
        print(f"[-]: {error_message}")
        with open(self.log_file, "a") as f:
            f.write(f"[ERROR]({self.current_datetime}): {error_message}\n")
            
            
nzbprolog = NzbProLogs()

API_ID = environ.get("API_ID", "")
API_HASH = environ.get("API_HASH", "")

BOT_TOKEN = environ.get("BOT_TOKEN", "")
BOT_TOKEN = BOT_TOKEN if BOT_TOKEN else nzbprolog.error("BOT_TOKEN is missing") or exit(1)

OWNER_ID = environ.get("OWNER_ID", "")
OWNER_ID = OWNER_ID if OWNER_ID else nzbprolog.error("OWNER_ID is missing") or exit(1)

AUTH_CHAT = environ.get("AUTH_CHAT", "")
AUTH_CHAT = int(AUTH_CHAT) if AUTH_CHAT else nzbprolog.error("AUTH_CHAT is missing") or exit(1)

H_IP = environ.get("H_IP", "")
H_IP = H_IP if H_IP else nzbprolog.error("H_IP is missing") or exit(1)

H_PORT = environ.get("H_PORT", "")
H_PORT = H_PORT if H_PORT else nzbprolog.error("H_PORT is missing") or exit(1)

H_API_KEY = environ.get("H_API_KEY", "")
H_API_KEY = H_API_KEY if H_API_KEY else nzbprolog.error("H_API_KEY is missing") or exit(1)

S_IP = environ.get("S_IP", "")
S_IP = S_IP if S_IP else nzbprolog.error("S_IP is missing") or exit(1)

S_PORT = environ.get("S_PORT", "")
S_PORT = S_PORT if S_PORT else nzbprolog.error("S_PORT is missing") or exit(1)

S_API_KEY = environ.get("S_API_KEY", "")
S_API_KEY = S_API_KEY if S_API_KEY else nzbprolog.error("S_API_KEY is missing") or exit(1)


NZB_URL    = f"http://{H_IP}:{H_PORT}/getnzb/user"
H_ENDPOINT = f"http://{H_IP}:{H_PORT}/api?apikey={H_API_KEY}"
H_INDEXERS = f"http://{H_IP}:{H_PORT}/api/stats?apikey={H_API_KEY}"
S_ENDPOINT = f"http://{S_IP}:{S_PORT}/sabnzbd/api?apikey={S_API_KEY}&output=json"

download_dict = {}

app = Client("nzbprobot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
nzbprolog.info("Starting Bot")
app.start()
BOT_NAME = app.get_me().first_name + (app.get_me().last_name or "")