from nzbpro import app
from asyncio import sleep
from telegraph import Telegraph
from aiohttp import ClientSession


class DownloadStatus:
    STATUS_WAITING = "Queued"
    STATUS_RUNNING = "Running"
    STATUS_FETCHING = "Fetching"
    STATUS_GRABBING = "Grabbing"
    STATUS_UPLOADING = "Uploading"
    STATUS_DOWNLOADING = "Downloading"
    STATUS_COMPLETED = "Completed"
    

async def set_interval(interval, func, *args, **kwargs):
    async def interval_wrapper():
        while True:
            try:
                await func(*args, **kwargs)
            except:
                pass
            await sleep(interval)

    return app.loop.create_task(interval_wrapper())


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


async def fetch_data(url, params=None, type=None):
    async with ClientSession() as session:
        async with session.get(url, params=params) as response:
            return (
                await response.json() if type == "dict" else await response.text()
            )


def progress_bar(percentage):
    n_blocks = 12
    f_blocks = round((int(percentage) / 100) * n_blocks)
    p_str = '■' * f_blocks
    p_str += '□' * (n_blocks - f_blocks)
    return f"[{p_str}]"
    
    
def get_status_msg(status, name, percentage, transferred, size, speed, eta, task_id):
    return (
        f"<strong>{status}</strong>: <code>{name}</code>\n"
        f"{progress_bar(percentage)} {int(percentage)}%\n"
        f"<strong>Processed</strong>: {transferred} of {size}\n"
        f"<strong>Speed</strong>: {speed} | <strong>ETA</strong>: {eta}\n"
        f"/cancel___{task_id}\n\n"
    )
    

def telegraph_page(query, items):
    title_content = f"<pre>Search Result for: <strong>{query}</strong></pre><br>"
    page_content = f"{title_content}{items}"
    response = telegraph.create_page(
        title="nzbprobot-search", author_name="nzbprobot", html_content=page_content
    )
    return response["url"]

telegraph = Telegraph(domain="graph.org")
telegraph.create_account(short_name="0xhellfire")