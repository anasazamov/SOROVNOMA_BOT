import logging
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from backend.adminbot.callback_func import *
from backend.adminbot.conversation_func import OPTION2, QUESTION1, question_create, option_create

# Bot tokeningizni kiriting
TOKEN = '6174496827:AAHJb6JtqS5ZH2KHUgLkf_kSc-aR1vnmm-Q'

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

    conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(filter_callback_data)],
    states={
        BOT_TOKEN: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_bot_token)],
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
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(filter_callback_data))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()

if __name__ == '__main__':
    main(TOKEN)
