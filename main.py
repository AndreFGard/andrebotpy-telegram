#!/usr/bin/python

# This is a simple echo app using the decorator mechanism.
# It echoes any incoming text messages.
import asyncio
import sys, os
sys.path.append("andrebotpy")
#import Andrebot
import andrebotpy.Andrebot

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

import interface

app = AsyncTeleBot(os.getenv('BOT_TOKEN'),)

# Handle '/start' and '/help'
#app_message_handler = lambda text


@app.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = """Hi, im Andrebotpy on telegram! this bot is still in beta, but it\'s \"stable\"
    release can be found in it\'s 'discord bot form. i dont know, however, how to  provide
    a link to it. In fact, thats why i created a telegram version!""".replace("\n", "")

    await app.reply_to(message, text)

### import all the functionality from my discord bot, andrebotpy
telegram_interface = lambda dec: interface.Telegram_Interface(app, dec)
andrebot = andrebotpy.Andrebot.Andrebot(app.message_handler, telegram_interface, "andrebotpy/")
asyncio.run(andrebot.create_functions())



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@app.message_handler(func=lambda message: True)
async def echo_message(message):
    ctx = interface.Telegram_Context_Adapter(app, message)
    await ctx.send(message.text)
    #await app.reply_to(message, message.text)





asyncio.run(app.polling())