from telegram.ext import Application
import os
import asyncio

async def main(token):
    application = Application.builder().token(token).build()
    domen = f"https://surway.samtuit.uz/api/"
    set_webhook_info = await application.bot.set_webhook(domen)


if __name__ == "__main__":
    asyncio.run(main("6174496827:AAHJb6JtqS5ZH2KHUgLkf_kSc-aR1vnmm-Q"))
