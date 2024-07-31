from telegram.ext import Application
import os
import asyncio

async def main():
    TOKEN = "6203772715:AAEV1XrdPUOdh6GfkTetPskKgE9jjMNaalQ"
    application = Application.builder().token(TOKEN).build()
    domen = f"https://bitcoin2.pythonanywhere.com/"
    await application.bot.delete_webhook()
    set_webhook_info = await application.bot.set_webhook(domen)


if __name__ == "__main__":
    asyncio.run(main())
