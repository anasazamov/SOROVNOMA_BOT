from telegram import Update
from telegram.ext import CallbackContext

async def help(update: Update, context: CallbackContext):
    """Send a message when the click qo' is issued."""
    await update.message.reply_text('Help!')