import logging
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from telegram import Update
# from backend.user_bot.callback_func import *
from backend.user_bot.callback_func import start, filter_callback_data, question
import os
import django
# Bot tokeningizni kiriting
TOKEN = '6174496827:AAHJb6JtqS5ZH2KHUgLkf_kSc-aR1vnmm-Q'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sorovnoma.settings')
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
    
 
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(filter_callback_data))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_handler(MessageHandler(filters.Text("Ovoz Berish"), question))

    application.run_polling()

if __name__ == '__main__':
    main(TOKEN)
