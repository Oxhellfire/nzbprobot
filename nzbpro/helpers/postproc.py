#!/usr/bin/python3

import sys
from re import findall
from shutil import rmtree
from requests import post
from dotenv import load_dotenv
from os import walk, path, environ
from subprocess import Popen, PIPE
from logging import basicConfig, FileHandler, StreamHandler, INFO, getLogger


try:
    directory = sys.argv[1]
except:
    print("No commandline parameters found")
    sys.exit(1)

load_dotenv("/root/config.env")

LOGFILE = "/root/.sabnzbd/logs/sabnzbd.log"
DEST_PATH = ""
RCLONE_NAME = "nzbpro"
NAME = environ["SAB_FINAL_NAME"]
BOT_TOKEN = environ['BOT_TOKEN']
AUTH_CHAT = environ['AUTH_CHAT']


basicConfig(format='%(message)s',
    handlers=[
        FileHandler(LOGFILE),
        StreamHandler()
    ],
    level=INFO
)

logger = getLogger(__name__)


def get_size(bytes):
    if bytes is None:
        return "0B"
    index = 0
    while bytes >= 1024:
        bytes /= 1024
        index += 1
    try:
        return f'{round(bytes, 2)} {["B", "KiB", "MiB", "GiB", "TiB", "PiB"][index]}'
    except IndexError:
        return "File too large"


def get_directory_size(directory):
    size = 0
    for dirpath, _, filenames in walk(directory):
        for filename in filenames:
            filepath = path.join(dirpath, filename)
            size += path.getsize(filepath)
    return size


def send_tg_message(drive_link):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    size = get_size(get_directory_size(directory))
    params = {
        'chat_id': AUTH_CHAT,
        'text': f"{NAME}\n{size}",
        'reply_markup': {
        "inline_keyboard": [
                [{"text": "Download", "url": drive_link}]
            ]
        }
    }
    
    res = post(api_url, json=params)
    if res.status_code == 200:
        sys.exit(0)

def subprocess_run(cmd):
    return Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)

exclude_list = ['.zip$', '.tar$', '.gz$', '.rar$', '^_UNPACK_']
exclude = ' '.join([f"--exclude '*{excl}'" for excl in exclude_list])
cmd = f"rclone copy '{directory}' '{RCLONE_NAME}:{DEST_PATH}/{NAME}' -P {exclude}"
process_copy = subprocess_run(cmd)


while True:
    line = process_copy.stdout.readline()
    if not line:
        break

    if match := findall(r'.+:\s+([\d.]+.\w+).\/.([\d.]+.\w+)..(\d+)...([\d.]+.\w+..)..\w+.(\d\w+)', line):
        logger.info(match[0])

process_copy.wait()

if process_copy.returncode == 0:
    cmd = f"rclone link '{RCLONE_NAME}:{DEST_PATH}/{NAME}'"
    link = subprocess_run(cmd)
    drive_link, _ = link.communicate()
    send_tg_message(drive_link)
    rmtree(directory)
else:
    print(f"rclone copy failed {process_copy.returncode, process_copy.stderr}")