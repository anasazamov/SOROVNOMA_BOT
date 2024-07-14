import os
import django
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot as bot1
from telegram.ext import CallbackContext, ConversationHandler
from asgiref.sync import sync_to_async
import logging
from .callback_func import *
from requests import get

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sorovnoma.settings')
django.setup()

from backend.models import Question, Options, Bot, BotAdmin, REQUIRED_CHANNELS, Bot, BotAdmin
from .check_bot import check_bot_token
logger = logging.getLogger(__name__)
# Stages
QUESTION1, OPTION2, BOT_TOKEN, CHANEL_NAME, BOT_CHANELS = range(5)

# Entry Point for the Conversation
async def start_conversation_quiz(update: Update, context: CallbackContext):
    
    data = update.callback_query.data.split(":")
    token = data[1]+":"+data[2]

    context.user_data['token'] = token
    await update.callback_query.message.reply_text("<b>So'rovnoma so'rovini yozing:</b>", parse_mode="HTML",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Bekor Qilish",callback_data=f"cancel_quiz:{token}")]]))
    return QUESTION1

# Get Bot Token and Validate
async def question_create(update: Update, context: CallbackContext):
    token = context.user_data['token']
    question_ = update.message.text
    bot = await sync_to_async(Bot.objects.get)(token=token)

    question_id = await sync_to_async(Question.objects.create)(bot=bot, name=question_)
    question_id = question_id.pk
    context.user_data["question_id"] = question_id

    await update.message.reply_html("<b>So'rovnoma so'rovi qabul qilindi. So'rovnoma variantlarini kiriting:</b>")        
    return OPTION2
    

async def option_create(update: Update, context: CallbackContext):

    option = update.message.text
    question_id = context.user_data['question_id']
    question_ = await sync_to_async(Question.objects.get)(id=question_id)
    token = context.user_data["token"]

    option = await sync_to_async(Options.objects.create)(option=option)

    await sync_to_async(question_.option.add)(option)
    await sync_to_async(question_.save)()

    button = [
        [InlineKeyboardButton(text="So'rovnoma yaratishni yakunlash",callback_data=f"cancel_quiz:{token}")]
    ]

    await update.message.reply_html("<b>So'rovnoma varianti qo'shildi</b>\nVarian qo'shish uchun davom eting:",reply_markup=InlineKeyboardMarkup(button))

    return OPTION2

# Cancel the Conversation
async def cancel_quiz(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat_id
    data = update.callback_query.data.split(":")
    token = data[1]+":"+data[2]
    buttons = [
        [InlineKeyboardButton("Ortga Qaytish",callback_data=f"quizes:{token}")],
        [InlineKeyboardButton("Bosh Menyuga Qaytish",callback_data="main menu")],
        ]
    await context.bot.edit_message_text(chat_id=chat_id,text="So'rovnoma yaratish yakunlandi!!!",reply_markup=InlineKeyboardMarkup(buttons),message_id=update.callback_query.message.message_id)
    return ConversationHandler.END

# Entry Point for the Conversation
async def start_conversation(update: Update, context: CallbackContext):
    
    await update.callback_query.message.reply_text("<b>Bot tokeni kiriting:</b>", parse_mode="HTML",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Bekor Qilish",callback_data="cancel")]]))
    return BOT_TOKEN

# Get Bot Token and Validate
async def get_bot_token(update: Update, context: CallbackContext):
    
    bot_token = update.message.text
    bot_info = await check_bot_token(bot_token)

    if bot_info[0]:
        is_exists_token = await sync_to_async(Bot.objects.filter(token=bot_token).exists)()
        if is_exists_token:
            
            await update.message.reply_text("<b>Bu tokenni avval ulagansiz boshqa token kiriting!!!</b>",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Bekor Qilish",callback_data="cancel")]]),parse_mode="HTML")
            return BOT_TOKEN
    
        context.user_data['bot_token'] = bot_token
        bot_name = bot_info[1]

        # Get the chat_id to associate the bot with the admin
        chat_id = update.message.chat_id
        bot_admin = await sync_to_async(BotAdmin.objects.get)(chat_id=chat_id)

        # Save Bot to the Database
        bot = await sync_to_async(Bot.objects.create)(
            name=bot_name,
            token=context.user_data['bot_token'],
            bot_admin=bot_admin
        )
        bot = bot1(context.user_data['bot_token'])
        bot.set_webhook(f"https://samtuit.pythonanywhere.com/api/{context.user_data['bot_token']}")
        buttons = [
            [InlineKeyboardButton(bot.name,callback_data=f"bot:{bot.token}")],
            [InlineKeyboardButton("Bosh Menyuga Qaytish",callback_data="main menu")]
            
            ]

        await update.message.reply_text("Bot muvaffaqiyatli qo'shildi!\nBotdan foydalanish uchun kanal nomini kiriting:",reply_markup=InlineKeyboardMarkup(buttons),parse_mode="HTML")
        return CHANEL_NAME
    else:
        await update.message.reply_text("Noto'g'ri token. Qayta urining:")
        return BOT_TOKEN

async def get_chanel_name(update: Update, context: CallbackContext):

    await update.message.reply_html("Botdan foydalanish uchun obuna bo'lish kerak bo'lgan kanalning IDsi yoki usernameni yuboring.\n Misol uchun: \n<b>@username</b>,\n<b><code>464654654</code></b>")
    context.user_data['chanel'] = update.message.text
    return BOT_CHANELS

async def bot_chanels(update: Update, context: CallbackContext):

    chanel_link = update.message.text.replace("@","")
    chanel = context.user_data["chanel"]
    token=context.user_data['bot_token']
    bot = await sync_to_async(Bot.objects.get)(token=token)
    
    buttons = [
                [InlineKeyboardButton(text="Kanal qo'shishnni to'xtatish",callback_data="cancel")]
            ]
    
    
    if "https" in chanel_link.split(":"):
        response = get(chanel_link)
        if response.status_code == 200:
            try:
                channel_id = context.user_data["channel_id"]
                chanel = await sync_to_async(REQUIRED_CHANNELS.objects.get)(id=channel_id)
                chanel.channel_link = chanel_link
                await sync_to_async(chanel.save)()
            except:
                await update.message.reply_html("<b>Xato!!! Avval kanal IDsini kiriting:</b>",reply_markup=InlineKeyboardMarkup(buttons))
                return BOT_CHANELS

            await update.message.reply_html("<b>Kanal muvaqqiyatli qo'shildi. Yana kanal qo'shishni hohlaysizmi?\nKanal nomini kiriting:</b>",reply_markup=InlineKeyboardMarkup(buttons))
            return CHANEL_NAME
        else:
            update.message.reply_html("<b>Yuborgan havolangiz yaroqsiz</b>",reply_markup=InlineKeyboardMarkup(buttons))
            return BOT_CHANELS
        
    elif chanel_link.isnumeric():
        chanel_obj = await sync_to_async(REQUIRED_CHANNELS.objects.create)(bot=bot,channel_id=chanel_link,channel=chanel)
        chanel_pk = chanel_obj.pk
        context.user_data['channel_id'] = chanel_pk
        await update.message.reply_html("<b>Kanal IDsi qabul qilidi!!!\nKanal qo'shilish havolasini yuboring\nMisol uchun:\nhttps://t.me/+JIbjbjhbUJHVHJvbhjb554BVH</b>")
        return BOT_CHANELS
    else:
        response = get(f"https://t.me/{chanel_link}")
        
        if response.status_code == 200:
            await sync_to_async(REQUIRED_CHANNELS.objects.create)(bot=bot,username=chanel_link,channel=chanel)
            await update.message.reply_html("<b>Kanal muvaqqiyatli qo'shildi. Yana kanal qo'shishni hohlaysizmi?\nKanal nomini kiriting:</b>",reply_markup=InlineKeyboardMarkup(buttons))
            return CHANEL_NAME
    
        await update.message.reply_html("<bYuborgan usernamemingiz yaroqsiz, tekshirib qaytadan yuboring!!!</b>",reply_markup=InlineKeyboardMarkup(buttons))
        return BOT_CHANELS
    

        

# Cancel the Conversation
async def cancel(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat_id
    await context.bot.edit_message_text(chat_id=chat_id,text="Bot qo'shish va botga kannal qo'shish to'xtatildi!!!",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Bosh Menyuga Qaytish",callback_data="main menu")]]),message_id=update.callback_query.message.message_id)
    return ConversationHandler.END