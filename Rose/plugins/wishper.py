from typing import Optional
from Rose import app
from pyrogram import filters, emoji
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid, MessageNotModified
)
from pyrogram.types import (
    User,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery,
    ChosenInlineResult
)

import json

try:
    with open('data.json') as f:
        whispers = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    whispers = {}
open('data.json', 'w').close()


lengths = 200
IMG = "https://telegra.ph/file/8bb5ad38249514dbf72e6.jpg"


@app.on_inline_query()
async def wishper_ai(_, sz: InlineQuery):
    query = sz.query
    split = query.split(' ', 1)
    if query == '' or len(query) > lengths \
            or (query.startswith('@') and len(split) == 1):
        title = f"🔐 Write a whisper message"
        content = ("**Send whisper messages through inline mode**\n\n"
                   "Usage: `@szrosebot [@username|@] text`")
        description = "Usage: @szrosebot [@username|@] text"
        button = InlineKeyboardButton(
            "Learn more...",
            url="https://t.me/szrosebot?start=learn"
        )
    elif not query.startswith('@'):
        title = f"{emoji.EYE} Whisper once to the first one who open it"
        content = (
            f"{emoji.EYE} The first one who open the whisper can read it"
        )
        description = f"{emoji.SHUSHING_FACE} {query}"
        button = InlineKeyboardButton(
            f"🎯 show message",
            callback_data="show_whisper"
        )
    else:
        # Python 3.8+
        u_target = 'anyone' if (x := split[0]) == '@' else x
        title = f"🔒 A whisper message to {u_target}, Only he/she can open it."
        content = f"🔒 A whisper message to {u_target}, Only he/she can open it."
        description = f"{emoji.SHUSHING_FACE} {split[1]}"
        button = InlineKeyboardButton(
            f"{emoji.LOCKED_WITH_KEY} show message",
            callback_data="show_whisper"
        )
    switch_pm_text = f"{emoji.INFORMATION} Learn how to send whispers"
    switch_pm_parameter = "learn"
    await sz.answer(
        results=[
            InlineQueryResultArticle(
                title=title,
                input_message_content=InputTextMessageContent(content),
                description=description,
                thumb_url=IMG,
                reply_markup=InlineKeyboardMarkup([[button]])
            )
        ],
        switch_pm_text=switch_pm_text,
        switch_pm_parameter=switch_pm_parameter
    )


@app.on_chosen_inline_result()
async def chosen_inline_result(_, cir: ChosenInlineResult):
    query = cir.query
    split = query.split(' ', 1)
    len_split = len(split)
    if len_split == 0 or len(query) > lengths \
            or (query.startswith('@') and len(split) == 1):
        return
    if len_split == 2 and query.startswith('@'):
        receiver_uname, text = split[0][1:] or '@', split[1]
    else:
        receiver_uname, text = None, query
    sender_uid = cir.from_user.id
    inline_message_id = cir.inline_message_id
    whispers[inline_message_id] = {
        'sender_uid': sender_uid,
        'receiver_uname': receiver_uname,
        'text': text
    }


