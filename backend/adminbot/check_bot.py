from backend.models import REQUIRED_CHANNELS
from telegram import ChatMember
from telegram.ext import CallbackContext
from requests import get
import logger

async def check_bot_token(token) -> list:
    response = get(f'https://api.telegram.org/bot{token}/getMe')

    if response.status_code == 200:
        return [True,response.json()['result']['first_name']]
    else:
        return [False,False]

async def is_subscribed(context: CallbackContext, user_id: int, REQUIRED_CHANNELS: REQUIRED_CHANNELS) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status not in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                return False
        except Exception as e:
            logger.error(f"Error checking subscription for {user_id} in {channel}: {e}")
            return False
    return True