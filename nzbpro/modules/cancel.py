from asyncio import sleep
from pyrogram import filters
from nzbpro import app, download_dict
from nzbpro.helpers.sabnzbd import SabnzbdDownloader
from nzbpro.helpers.custom_filters import owner_only_command
from nzbpro.helpers.msg_utils import send_message, clear_tasks


sabnzbd = SabnzbdDownloader()

@app.on_message(filters.regex(r'/cancel___.*'))
async def cancel_task(_, message):
    task_id = message.text.split("@")[0].split("___")[1]
    queue_status = await sabnzbd.clear_queue(task_id)
    if queue_status is None:
        await sabnzbd.cancel_history_upload(task_id)
        await sleep(1)
        await sabnzbd.clear_history(task_id)
        
    await send_message(message, f"{task_id} Task Cancelled!")


@owner_only_command("cancelall")
async def cancel_all_task(_, message):
    chat_id = message.chat.id
    await sabnzbd.clear_all()
    if chat_id in list(download_dict.keys()):
        await clear_tasks(download_dict[chat_id])
    await send_message(message, "Cancelled all Tasks!")
