from telegram.ext import Application
import os

TOKEN = os.environ['TOKEN']
aplication = Application.builder().token(TOKEN).build()
domen = ""
aplication.bot.set_webhook(domen)