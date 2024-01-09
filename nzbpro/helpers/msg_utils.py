from nzbpro import download_dict
from pyrogram.enums import ParseMode
from nzbpro.helpers.extra_utils import set_interval
from nzbpro.helpers.sabnzbd import SabnzbdDownloader


sabnzbd = SabnzbdDownloader()

async def send_message(message, text, keyboard=None):
    try:
        return await message.reply(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"SOMETHING WENT WRONG = send_message =: {e}")


async def edit_message(message, text):
    try:
        await message.edit(
            text=text,
            parse_mode=ParseMode.HTML
        )
    except:
        pass


async def delete_message(message):
    try:
        await message.delete()
    except Exception as e:
        print(f"SOMETHING WENT WRONG = delete_message =: {e}")


async def clear_tasks(message):
    chat_id = message.chat.id
    if chat_id in list(download_dict.keys()):
        try:
            await delete_message(message)
            del download_dict[chat_id]
        except:
            pass


async def update_all_messages():
    progress_status  = await sabnzbd.onDlProgress()
    for chat_id in list(download_dict.keys()):
        if not progress_status:
            await clear_tasks(download_dict[chat_id])
            return True
        if download_dict[chat_id] and progress_status != download_dict[chat_id].text:
            try:
                await edit_message(download_dict[chat_id], progress_status)
            except:
                pass
            download_dict[chat_id].text = progress_status


async def send_status_message(message):
    chat_id = message.chat.id
    if chat_id in list(download_dict.keys()):
        try:
            old_status = download_dict[chat_id]
            await clear_tasks(old_status)
        except Exception as e:
            print(f"SOMETHING WENT WRONG = send_status_message =: {e}")
            
    progress_status  = await sabnzbd.onDlProgress()
    empty_status = await send_message(message, progress_status)
    download_dict[chat_id] = empty_status
    await set_interval(8, update_all_messages)
