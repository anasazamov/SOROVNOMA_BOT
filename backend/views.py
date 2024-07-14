from django.http import HttpRequest, HttpResponse
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from .adminbot.callback_func import *
import json
import requests as req

# Create your views here.

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Kechirasiz, bu komanda tanilmagan. Iltimos, /start komandasidan foydalaning.')

TOKEN = "6174496827:AAHJb6JtqS5ZH2KHUgLkf_kSc-aR1vnmm-Q"
application = Application.builder().token(TOKEN).build()

def send_message(data):
    URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = req.post(URL, data={"chat_id": 1698951222, "text": f"{data}"})

async def telegram(request: HttpRequest) -> HttpResponse:
    """Handle incoming Telegram updates by putting them into the `update_queue`"""

    # Extract the update from the request body
    update_data = json.loads(request.body.decode())
    update = Update.de_json(update_data, application.bot)

    # Define your conversation handler
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

    # Add handlers to the application
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(filter_callback_data))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Initialize the application
    await application.initialize()

    # Put the update in the queue
    await application.update_queue.put(update)

    # Process the update
    await application.process_update(update)

    return HttpResponse()

