import os
import django
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Bot as bot1
from telegram.ext import CallbackContext
from backend.user_bot.is_subscribed_func import is_subscribed
from asgiref.sync import sync_to_async

# Django muhitini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from backend.models import Bot, REQUIRED_CHANNELS, Voter, Question, Options

async def requirements_chanels(update: Update, context: CallbackContext, channels):
    buttons = []
    for channel_dict in channels:
        buttons.append([InlineKeyboardButton(text=channel_dict["name"], url=channel_dict["channel_link"])])
    buttons.append([InlineKeyboardButton(text="Tekshirish ✅", callback_data="checked_chanels")])

    if update.callback_query:
        
        chat_id = update.callback_query.message.chat_id
        
        await context.bot.send_message(text="<b>Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling</b>", reply_markup=InlineKeyboardMarkup(buttons),chat_id=chat_id,parse_mode="HTML")

    elif update.message:
        await update.message.reply_html(text="<b>Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling</b>", reply_markup=InlineKeyboardMarkup(buttons))


    
async def check_chanels(channel_data: REQUIRED_CHANNELS, context: CallbackContext, user_id):
    channels_username = []
    for channel in channel_data:
        if channel.username:
            channels_username.append(channel.username)
        elif channel.channel_id:
            channels_username.append(int(f"-100{channel.channel_id}"))

    if channels_username:
        list_chanel = await is_subscribed(context, user_id, channels_username)
        not_subscription = []
        for channel_index in list_chanel:
            if type(channel_index) == int:
                channel_obj = await sync_to_async(list)(REQUIRED_CHANNELS.objects.filter(channel_id=int(f"{channel_index}".replace("-100",""))))
                channel_obj = channel_obj[0]
                dict_ = {
                    "name": channel_obj.channel,
                    "channel_link": channel_obj.channel_link
                }
                not_subscription.append(dict_)
            elif channel_index:
                channel_obj = await sync_to_async(list)(REQUIRED_CHANNELS.objects.filter(username=channel_index.replace("@","")))
                channel_obj = channel_obj[0]
                dict_ = {
                    "name": channel_obj.channel,
                    "channel_link": f"https://t.me/{channel_obj.username}"
                }
                not_subscription.append(dict_)

        return not_subscription
    return False

async def start2(update: Update, context: CallbackContext):
    token = context.bot.token
    bot = await sync_to_async(Bot.objects.get)(token=token)
    required_channels_qs = await sync_to_async(list)(REQUIRED_CHANNELS.objects.filter(bot=bot))
    if update.callback_query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
        message = update.callback_query.message
        await context.bot.delete_message(chat_id=chat_id,message_id=message_id)
    elif update.message:
        chat_id = update.message.chat_id
        message = update.message
    chanels = await check_chanels(required_channels_qs, context, chat_id)

    if chanels:
        return await requirements_chanels(update, context, chanels)
    
    first_name = message.chat.full_name
    username = message.chat.username
    if not username:
        username = " "
    is_exists_voter = await sync_to_async(Voter.objects.filter(chat_id=chat_id).exists)()
    
    if not is_exists_voter:
        await sync_to_async(Voter.objects.create)(first_name=first_name,username=username,chat_id=chat_id,bot=bot)
    
    await message.reply_html("<b>Аssalomu Аlaykum.\n🙂 Soʼrovnoma botga xush kelibsiz!</b>",reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Ovoz Berish")]],resize_keyboard=True))

async def question2(update: Update, context: CallbackContext):
    token = context.bot.token
    bot = await sync_to_async(Bot.objects.get)(token=token)
    required_channels_qs = await sync_to_async(list)(REQUIRED_CHANNELS.objects.filter(bot=bot))
    if update.callback_query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
        message = update.callback_query.message

        await context.bot.delete_message(chat_id=chat_id,message_id=message_id)
    elif update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        message = update.message
    chanels = await check_chanels(required_channels_qs, context, chat_id)

    if chanels:
        return await requirements_chanels(update, context, chanels)
    
    voter = await sync_to_async(Voter.objects.get)(chat_id=chat_id)
    questions = await sync_to_async(list)(Question.objects.filter(bot=bot, is_active=True).exclude(voter=voter))
    
    if questions:
        question_0 = questions[0]
        question_id = question_0.pk
        is_exist_other_q = 1
    else:
        is_exist_other_q = 0
    
    if is_exist_other_q: 
        buttons = []
        options = await sync_to_async(list)(question_0.option.all())
        for option in options:
            name = option.option
            option_pk = option.pk
            total_vote = option.total_vote
            # Switch inline query ni boshqa chatlar uchun ham ko'rinadigan qilib o'rnatish
            buttons.append([
                InlineKeyboardButton(
                    text=f"{name} - {total_vote}",
                    callback_data=f"select_option:{question_id}:{option_pk}:{is_exist_other_q}",
                    switch_inline_query_current_chat=f"{name}"  # Yoki switch_inline_query=f"{name}"
                )
            ])
        
        return await context.bot.send_message(
            text=f"<b>{question_0.name}</b>", 
            reply_markup=InlineKeyboardMarkup(buttons),
            chat_id=chat_id,
            parse_mode="HTML"
        )
    
    await context.bot.send_message(
        chat_id=chat_id,
        text="<b>Barcha so'rovnomalarga javob berib bo'lgansiz</b>",
        parse_mode="HTML"
    )
async def select_option(update: Update, context: CallbackContext):

    data = update.callback_query.data.split(":")
    question_id = int(data[1])
    option_id = int(data[2])
    is_exist_other_q = int(data[3])
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id

    question_obj = await sync_to_async(Question.objects.get)(id=question_id)
    option_obj = await sync_to_async(Options.objects.get)(id=option_id)
    voter_obj = await sync_to_async(Voter.objects.get)(chat_id=chat_id)

    is_exists_voter = await sync_to_async(question_obj.option.filter(votes=voter_obj).exists)()
    if is_exists_voter:
        return await update.callback_query.message.reply_html("<b>Barcha so'rovnomalarga javob berib bo'lgansiz!!!</b>")

    option_obj.total_vote = option_obj.total_vote + 1
    await sync_to_async(option_obj.votes.add)(voter_obj)
    await sync_to_async(option_obj.save)()

    await sync_to_async(question_obj.voter.add)(voter_obj)
    await sync_to_async(question_obj.save)()

    if is_exist_other_q:
        return await question2(update,context)
    await context.bot.delete_message(chat_id=chat_id,message_id=message_id)
    await update.callback_query.message.reply_html("<b>Barcha so'rovnomalarga javob berib bo'lgansiz!!!</b>")

async def filter_callback_data2(update: Update, context: CallbackContext):

    data = update.callback_query.data

    if data == "checked_chanels":
        await start2(update,context)
    elif "select_option" in data.split(":"):
        await select_option(update,context)
    