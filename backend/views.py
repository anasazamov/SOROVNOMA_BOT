from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from .adminbot.callback_func import *
from asgiref.sync import sync_to_async
import os

# Create your views here.

async def unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Kechirasiz, bu komanda tanilmagan. Iltimos, /start komandasidan foydalaning.')

TOKEN = "6174496827:AAHJb6JtqS5ZH2KHUgLkf_kSc-aR1vnmm-Q"
application = Application.builder().token(TOKEN).build()

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

class AdminBot(APIView):

    def post(self, request, *args, **kwargs):
        update = Update.de_json(request.data, application.bot)
        application.process_update(update)
        return Response(status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        return Response({"message": "working"}, status=status.HTTP_200_OK)
