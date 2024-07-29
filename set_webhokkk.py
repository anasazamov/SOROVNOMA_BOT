from telegram.ext import Application
import os
import asyncio

async def main():
    TOKEN = "6174496827:AAHJb6JtqS5ZH2KHUgLkf_kSc-aR1vnmm-Q"
    application = Application.builder().token(TOKEN).build()
    domen = f"https://surway.samtuit.uz/api/"
    await application.bot.delete_webhook()
    set_webhook_info = await application.bot.set_webhook(domen)


if __name__ == "__main__":
    asyncio.run(main())
