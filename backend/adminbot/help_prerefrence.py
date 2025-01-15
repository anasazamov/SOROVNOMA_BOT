from telegram import Update
from telegram.ext import CallbackContext

async def help_func(update: Update, context: CallbackContext):
    """Send a message when the click qo' is issued."""
    await update.callback_query.message.reply_text('Ish jarayonida\n bosh sahifaga qaytish uchun /start ni bosing otish uchun /start ni bosing') 