import logging
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from telegram import Update
# from backend.user_bot.callback_func import *
from backend.user_bot.callback_func import start2, filter_callback_data2, question2
import os
import django
# Bot tokeningizni kiriting
TOKEN = '6668135627:AAG8Oig0yhosU8H342ULH-ZOwsupTPCXhi8'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Bot logs ini sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Unknown komandalar uchun handler
async def unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Kechirasiz, bu komanda tanilmagan. Iltimos, /start komandasidan foydalaning.')

# Asosiy funktsiya
def main(token) -> None:
    application = Application.builder().token(token).build()
    
 
    application.add_handler(CommandHandler("start", start2))
    application.add_handler(CallbackQueryHandler(filter_callback_data2))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_handler(MessageHandler(filters.Text("Ovoz Berish"), question2))

    application.run_polling()

if __name__ == '__main__':
    main(TOKEN)
