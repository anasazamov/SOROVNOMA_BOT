from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, Updater
from .adminbot.callback_func import *
import os
import requests as req

# Create your views here.

async def unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Kechirasiz, bu komanda tanilmagan. Iltimos, /start komandasidan foydalaning.')

TOKEN = "6174496827:AAHJb6JtqS5ZH2KHUgLkf_kSc-aR1vnmm-Q"
application = Application.builder().token(TOKEN).build()

def send_message(data):

    URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = req.post(URL,data={"chat_id":1698951222,"text": f"{data}"})



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


async def process_update_func(update):

    return await application.process_update(update)

class AdminBotView(APIView):

    def post(self, request, *args, **kwargs):
        
        send_message(request.data)
        update = Update.de_json(request.data, application.bot)
        # Update ni qayta ishlash
        process_update_func(update)
        
        return Response({"message":"OK"}, status=status.HTTP_200_OK)
        


    
    def get(self, request, *args, **kwargs):
        return Response({"message": "working"}, status=status.HTTP_200_OK)
