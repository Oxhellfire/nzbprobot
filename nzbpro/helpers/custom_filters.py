from pyrogram import filters
from nzbpro import app, OWNER_ID


def owner_only_filter(user_id):
    def func(_, __, message):
        return message.from_user and message.from_user.id == user_id
    return filters.create(func)

owner_only = owner_only_filter(OWNER_ID)

def owner_only_command(command):
    def decorator(func):
        @app.on_message(filters.command(command) & owner_only)
        def wrapper(_, message):
            func(_, message)
        return wrapper
    return decorator