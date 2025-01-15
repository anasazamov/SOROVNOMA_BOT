from django.http import HttpRequest, HttpResponse, JsonResponse
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from .adminbot.callback_func import *
from .user_bot.callback_func import *
from .adminbot.help_prerefrence import *
import json
import requests as req


# Create your views here.

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Kechirasiz, bu komanda tanilmagan. Iltimos, /start komandasidan foydalaning.')

TOKEN = "6174496827:AAHJb6JtqS5ZH2KHUgLkf_kSc-aR1vnmm-Q"
application = Application.builder().token(TOKEN).build()
conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(filter_callback_data)],
    states={
        BOT_TOKEN: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_bot_token)],
        START_CHANEL: [MessageHandler(filters.TEXT & (~filters.COMMAND), start_chanel)],
        CHANEL_NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_chanel_name)],
        BOT_CHANELS: [MessageHandler(filters.TEXT & (~filters.COMMAND), bot_chanels)],
        QUESTION1: [MessageHandler(filters.TEXT & (~filters.COMMAND), question_create)],
        OPTION2: [MessageHandler(filters.TEXT & (~filters.COMMAND), option_create)],
        START_FORWARD: [MessageHandler(filters.TEXT & (~filters.COMMAND), start_forwrad)],
        FORWARD_FOR_USER: [MessageHandler(filters.TEXT & (~filters.COMMAND), forward_for_user)],
        CANCEL_FORWARD: [MessageHandler(filters.TEXT & (~filters.COMMAND), cancel_forward)],
    },
    fallbacks=[CallbackQueryHandler(filter_callback_data)],
    allow_reentry=True,
)

# Add handlers to the application
application.add_handler(conv_handler)
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(help, pattern="help"))
application.add_handler(CallbackQueryHandler(filter_callback_data))
application.add_handler(MessageHandler(filters.COMMAND, unknown))

def send_message(data):
    URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = req.post(URL, data={"chat_id": 1698951222, "text": f"{data}"})

async def telegram(request: HttpRequest) -> HttpResponse:

    global DOMEN
    DOMEN = request.get_host()

    if request.method == "GET":   
        return JsonResponse({"message": f"this is route working in {DOMEN}"})

    # Extract the update from the request body
    update_data = json.loads(request.body.decode())
    update = Update.de_json(update_data, application.bot)
    #send_message(update_data)

    await application.initialize()

    await application.update_queue.put(update)

    await application.process_update(update)


    await application.shutdown()

    return HttpResponse({"message":"OK"})

async def telegram2(request: HttpRequest,token) -> HttpResponse:

    if request.method == "get":
        return JsonResponse({"message": "this is route working"})


    """Handle incoming Telegram updates by putting them into the `update_queue`"""
    application2 = Application.builder().token(token).build()

    # Extract the update from the request body
    update_data = json.loads(request.body.decode())
    update = Update.de_json(update_data, application2.bot)
    #send_message(update_data)
    # Define your conversation handler

    # Add handlers to the application2
    application2.add_handler(CommandHandler("start", start2))
    application2.add_handler(CallbackQueryHandler(filter_callback_data2))
    application2.add_handler(MessageHandler(filters.COMMAND, unknown))
    application2.add_handler(MessageHandler(filters.Text("Ovoz Berish"), question2))


    # Initialize the application2
    await application2.initialize()

    # Put the update in the queue
    await application2.update_queue.put(update)

    # Process the update
    await application2.process_update(update)


    await application2.shutdown()

    return HttpResponse({"message":"OK"})

