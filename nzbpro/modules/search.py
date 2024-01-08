from imdb import IMDb
from nzbpro import app
from pyrogram import filters
from re import search as re_search
from pykeyboard import InlineKeyboard
from pyrogram.types import InlineKeyboardButton as Ikb
from nzbpro.helpers.nzbhydra_apis import HydraHelper, INDEXERS_WEBSITES


ia = IMDb()
hydra = HydraHelper()

# Credit goes to https://github.com/TheHamkerCat/WilliamButcherBot/tree/dev/wbb/modules
def keyboard(buttons_list, row_width: int=2):
    buttons = InlineKeyboard(row_width=row_width)
    data = [Ikb(text=str(i[0]), url=str(i[1])) for i in buttons_list]
    buttons.add(*data)
    return buttons


def ikb(data: dict, row_width: int=2):
    return keyboard(data.items(), row_width=row_width)


@app.on_message(filters.command(["find", "f"]))
async def find(_, message):
    if len(message.command) < 2:
        await message.reply_text("Where is Query")
        return
    query = " ".join(message.command[1:])
    output = await hydra.query(query)
    await message.reply_text(f"**query for {query}**\n\n{output}")


@app.on_message(filters.command(["movie", "m"]))
async def movie(_, message):
    if len(message.command) < 2:
        await message.reply_text("Where is Query")
        return
    query = " ".join(message.command[1:])
    match = re_search(r'tt\d{4,}', query)
    if match:
        imdb_id = match.group()
        data = ia.get_movie(imdb_id[2:])
        title = data.get('title', 'N/A')
        output = await hydra.imdb_movie_query(imdb_id)
    else:
        output = await hydra.movie_query(query)
    await message.reply_text(f"**query for {title if match else query}**\n\n{output}")


@app.on_message(filters.command(["series", "s"]))
async def search(_, message):
    if len(message.command) < 2:
        await message.reply_text("Where is Query")
        return
    query = " ".join(message.command[1:])
    match = re_search(r'tt\d{4,}', query)
    if match:
        imdb_id = match.group()
        data = ia.get_movie(imdb_id[2:])
        title = data.get('title', 'N/A')
        output = await hydra.imdb_series_query(imdb_id)
    else:
        output = await hydra.series_query()(query)
    await message.reply_text(f"**query for {title if match else query}**\n\n{output}")


@app.on_message(filters.command(["book", "b"]))
async def book(_, message):
    if len(message.command) < 2:
        await message.reply_text("Where is Query")
        return
    query = " ".join(message.command[1:])
    output = await hydra.book_query(query)
    await message.reply_text(f"**query for {query}**\n\n{output}")


@app.on_message(filters.command(["indexers", "ind"]))
async def indexers(_, message):
    indexers = await hydra.indexers()
    buttons = keyboard([
        (indexer, INDEXERS_WEBSITES[indexer]) for indexer in indexers
    ])
    await message.reply_text(f"**Here are Your Indexers List**", reply_markup=buttons)
