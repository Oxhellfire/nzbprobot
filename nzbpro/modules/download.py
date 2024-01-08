from os import remove
from nzbpro import app
from pyrogram import filters
from nzbpro.helpers.sabnzbd import SabnzbdDownloader
from nzbpro.helpers.msg_utils import send_status_message, send_message


sabnzbd = SabnzbdDownloader()

@app.on_message(filters.command("add"))
async def sabnzbd_add(_, message):
    file = message.reply_to_message
    if file and file.document and file.document.mime_type == "application/x-nzb":
        file_path = await file.download()
        await sabnzbd.add_sabnzbd_download(file_path, None)
        remove(file_path)
    else:
        if len(message.command) < 2:
            await send_message(message, "I didn't Get Any NZB ID[s]")
            return

        nzo_ids = message.text.split()[1:]
        await sabnzbd.add_sabnzbd_download(None, nzo_ids)
    
    await send_status_message(message)