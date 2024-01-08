from os import path
from glob import glob
from uvloop import install
from pyrogram import idle, filters
from contextlib import closing, suppress
from nzbpro import NzbProLogs, BOT_NAME, app
from asyncio import get_event_loop, all_tasks, exceptions


nzbprolog = NzbProLogs()
loop = get_event_loop()

async def start_bot():
    modules = [
        file for file in glob(path.join("nzbpro/modules", '*.py'))
        if not path.basename(file).startswith('__')
    ]

    for module in modules:
        m_name = path.splitext(path.basename(module))[0]
        __import__(f'nzbpro.modules.{m_name}')
    
    nzbprolog.info("All Modules Loaded Successfully")
    nzbprolog.info(f"{BOT_NAME} Started")
    await idle()

    nzbprolog.info("Stopping app")
    await app.stop()
    
    nzbprolog.info("Terminating all asyncio tasks")
    for task in all_tasks():
        task.cancel()
    nzbprolog.info("Bot Stopped!")
    

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Hello from Bot")
    

if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(exceptions.CancelledError):
            loop.run_until_complete(start_bot())