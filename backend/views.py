from django.shortcuts import render
from rest_framework.views import Response, APIView, Request
from rest_framework import status
from telegram import Update, Bot, ChatMember
from telegram.ext import Updater, CommandHandler, filters, MessageHandler, Application, CallbackQueryHandler, ConversationHandler
from .adminbot.callback_func import *
import os
# Create your views here.

async def unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Kechirasiz, bu komanda tanilmagan. Iltimos, /start komandasidan foydalaning.')



TOKEN = os.environ["TOKEN"]
application = Application.builder().token(TOKEN).build()

class AdminBot(APIView):

    def post(self, request: Request, *args, **kwargs):
        update = Update.de_json(request.data, application.bot)
        application.process_update(update)
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
        return Response(status=status.HTTP_200_OK)


