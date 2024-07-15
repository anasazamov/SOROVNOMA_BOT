from telegram import ChatMember
from telegram.ext import CallbackContext

async def is_subscribed(context: CallbackContext, user_id: int, REQUIRED_CHANNELS) -> list:
    not_subscription = []
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status not in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
                not_subscription.append(channel)
        except Exception as e:
            
            not_subscription.append(channel)

    return not_subscription
