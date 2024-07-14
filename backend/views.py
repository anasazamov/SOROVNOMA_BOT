# views.py

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, CallbackContext, ContextTypes
import json
import requests as req

# Create your views here.

async def unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Kechirasiz, bu komanda tanilmagan. Iltimos, /start komandasidan foydalaning.')

TOKEN = "YOUR_BOT_TOKEN"
application = Application.builder().token(TOKEN).updater(None).context_types(ContextTypes(context=CallbackContext)).build()

def send_message(data):
    URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = req.post(URL, data={"chat_id":1698951222, "text": f"{data}"})

conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(filter_callback_data)],
    states={
        BOT_TOKEN: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_bot_token)],
        CHANEL_NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_chanel_name)],
        BOT_CHANELS: [MessageHandler(filters.TEXT & (~filters.COMMAND), bot_chanels)],  
        QUESTION1: [MessageHandler(filters.TEXT & (~filters.COMMAND), question_create)],
        OPTION2: [MessageHandler(filters.TEXT & (~filters.COMMAND), option_create)],      
    },
    fallbacks=[CallbackQueryHandler(filter_callback_data)],
    allow_reentry=True,
)

application.add_handler(conv_handler)
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(filter_callback_data))
application.add_handler(MessageHandler(filters.COMMAND, unknown))

async def telegram(request: HttpRequest) -> HttpResponse:
    """Handle incoming Telegram updates by putting them into the `update_queue`"""

    send_message(json.loads(request.body.decode()))

    await application.update_queue.put(
        Update.de_json(data=json.loads(request.body.decode()), bot=application.bot)
    )
    return HttpResponse()
