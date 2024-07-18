import os
import django
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton,Bot as bot1
from telegram.ext import CallbackContext, ConversationHandler
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from backend.models import BotAdmin, Bot, Question, REQUIRED_CHANNELS
from .conversation_func import *
from .test import write_survey_results_to_csv
from requests import get
async def start(update: Update, context: CallbackContext):
    
    if update.message:
        chat_id = update.message.chat_id
        username = update.message.from_user.username
        first_name = update.message.from_user.first_name
        last_name = update.message.from_user.last_name
    elif update.callback_query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
        inline_keyboard = [
            [InlineKeyboardButton(text="Mening botlarim", callback_data="Mening Botlarim")],
            [InlineKeyboardButton(text="Bot Yaratish", callback_data="Bot Yaratish")]
        ]
        await context.bot.edit_message_text(chat_id=chat_id,
            text="<b>Bosh Menyu</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard),
            parse_mode="HTML",
            message_id=message_id)
        
        return 0
    

    try:
        admin = await sync_to_async(BotAdmin.objects.get)(chat_id=chat_id)
        inline_keyboard = [
            [InlineKeyboardButton(text="Mening botlarim", callback_data="Mening Botlarim")],
            [InlineKeyboardButton(text="Bot Yaratish", callback_data="Bot Yaratish")]
        ]
        await context.bot.send_message(chat_id=chat_id,
            text="Assalom Alaykum. Qayta Xush kelibsiz",
            reply_markup=InlineKeyboardMarkup(inline_keyboard))
    except BotAdmin.DoesNotExist:
        admin = await sync_to_async(BotAdmin.objects.create)(
            first_name=first_name,
            last_name=last_name,
            chat_id=chat_id,
            username=username
        )
        inline_keyboard = [
            [InlineKeyboardButton(text="Mening botlarim", callback_data="Mening Botlarim")],
            [InlineKeyboardButton(text="Bot Yaratish", callback_data="Bot Yaratish")]
        ]
        await update.message.reply_html(
            "Assalom Alaykum. Xush kelibsiz O'z so'rovnoma botingizni yaratish uchun <b>Bot Yaratish</b> tugmasini bosing",
            reply_markup=InlineKeyboardMarkup(inline_keyboard)
        )

async def mybot(update: Update, context: CallbackContext):
    
    if update.message:
        chat_id = update.message.chat_id
    elif update.callback_query:
        chat_id = update.callback_query.message.chat_id

    bot_admin = await sync_to_async(BotAdmin.objects.get)(chat_id=chat_id)
    my_bots = await sync_to_async(list)(Bot.objects.filter(bot_admin=bot_admin))

    buttons = []
    if my_bots:
        for bot in my_bots:
            buttons.append([InlineKeyboardButton(bot.name, callback_data=f"bot:{bot.token}")])
        buttons.append([InlineKeyboardButton("Ortga Qaytish", callback_data="back:start")])

        
        if update.callback_query:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=update.callback_query.message.message_id,
                text="<b>Sizning Botlaringiz:</b>",
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode="HTML"
            )
    else:
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=update.callback_query.message.message_id,
            text="Siz hali botlar yaratmagansiz.\nBot Yaratish uchun <b>Bot Yaratish Tugmasini Bosing</b>", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Bot Yaratish", callback_data="Bot Yaratish")],[InlineKeyboardButton("Ortga Qaytish", callback_data="back:start")]]), 
            parse_mode="HTML"
        )

async def select_bot(update: Update, context: CallbackContext):

    data = update.callback_query.data.split(":")
    token = data[1]+":"+data[2]
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id
    text = "<b>Bot Sozlanmalari</b>"
    buttons = [
        [InlineKeyboardButton(text="So'rovnomalar",callback_data=f"quizes:{token}"),
        InlineKeyboardButton(text="Bot kanallari",callback_data=f"channels:{token}")],
        [InlineKeyboardButton("Ortga Qaytish",callback_data=f"Mening Botlarim"),
        InlineKeyboardButton("Bosh Menyuga Qaytish",callback_data="main menu")],
        [InlineKeyboardButton("Botni O'chirish",callback_data=f"delete_bot:{token}")] ,
        # [InlineKeyboardButton(text="Obunachilarga xabar yuborish", callback_data=f"start_forward:{token}")]
    ]
    await context.bot.edit_message_text(chat_id=chat_id,text=text,message_id=message_id,reply_markup=InlineKeyboardMarkup(buttons),parse_mode="HTML")

async def quizes(update: Update, context: CallbackContext):

    data =update.callback_query.data.split(":")
    token = data[1]+":"+data[2]
    bot = await sync_to_async(Bot.objects.get)(token=token)
    message_id = update.callback_query.message.message_id
    chat_id = update.callback_query.message.chat_id
    text = "<b>So'rovnomalaringiz:</b>"
    questions = await sync_to_async(list)(Question.objects.filter(bot=bot))
    buttons = []
    if not questions:
        text = "<b>Siz hozirda so'rovnoma yaratmagansiz!!!</b>"
    for question in questions:
        buttons.append([InlineKeyboardButton(question.name,callback_data=f'select_quiz:{question.pk}')])
    
    buttons.append([InlineKeyboardButton("So'rovnoma Yaratish",callback_data=f"create_quiz:{token}")])
    buttons[-1].append(InlineKeyboardButton("Ortga Qaytish",callback_data=f"bot:{token}"))
    buttons.append([InlineKeyboardButton("Bosh Menyuga Qaytish",callback_data="main menu")])
    await context.bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=text,parse_mode="HTML",reply_markup=InlineKeyboardMarkup(buttons))
    # await update.callback_query.message.reply_text("So'rovnoma yaratish uchun quyidagi tugmani bosing",reply_markup=ReplyKeyboardMarkup([[KeyboardButton("So'rovnoma Yaratish")]],resize_keyboard=True))
    
async def bot_chanels_func(update: Update, context: CallbackContext):

    data =update.callback_query.data.split(":")
    token = data[1]+":"+data[2]
    bot = await sync_to_async(Bot.objects.get)(token=token)
    message_id = update.callback_query.message.message_id
    chat_id = update.callback_query.message.chat_id
    text = "<b>Bot Adminlik qilayotgan kanallar:</b>"
    questions = await sync_to_async(list)(REQUIRED_CHANNELS.objects.filter(bot=bot))
    buttons = []
    if not questions:
        text = "<b>Siz hozirda kanal qo'shmagansiz!!!</b>"
    for question in questions:
        buttons.append([InlineKeyboardButton(question.channel,callback_data=f'select_chanel:{question.pk}')])
    
    buttons.append([InlineKeyboardButton("Ortga Qaytish",callback_data=f"bot:{token}")])
    buttons.append([InlineKeyboardButton("Bosh Menyuga Qaytish",callback_data="main menu")])
    await context.bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=text,parse_mode="HTML",reply_markup=InlineKeyboardMarkup(buttons))

async def select_quiz(update: Update, context: CallbackContext):

    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id

    question_id = update.callback_query.data.split(":")[1]
    question = await sync_to_async(Question.objects.get)(id=question_id)
    bot = await sync_to_async(lambda: question.bot)()
    token = bot.token
    button = []
    text = f'<b>{question.name}</b>'
    options = await sync_to_async(list)(question.option.all())

    for option in options:
        text += f"\n{option.option} Jami ovoz: {option.total_vote}"
    
    is_active = question.is_active
    if is_active:
        active_text = "So'rovnoma faol"
    else:
        active_text = "So'rovnoma nofaol"

    button.append([InlineKeyboardButton(active_text,callback_data=f"active_quiz:{question.pk}")])
    button.append([InlineKeyboardButton("So'rovnomani o'chirish",callback_data=f"delete_quiz:{question.pk}")])  
    button.append([InlineKeyboardButton(text="Ortga Qaytish",callback_data=f"quizes:{token}")]) 
    button.append([InlineKeyboardButton("So'rovnoma natijalarni yuklab olish",callback_data=f"download_quiz:{question.pk}")])
    await context.bot.edit_message_text(chat_id=chat_id,text=text,reply_markup=InlineKeyboardMarkup(button),parse_mode="HTML",message_id=message_id)

async def active_quiz(update: Update, context: CallbackContext):

    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id


    question_id = update.callback_query.data.split(":")[1]
    question = await sync_to_async(Question.objects.get)(id=question_id)
    bot = await sync_to_async(lambda: question.bot)()
    token = bot.token
    button = []
    text = f'<b>{question.name}</b>'
    options = await sync_to_async(list)(question.option.all())

    for option in options:
        text += f"\n{option.option} Jami ovoz: {option.total_vote}"
    
    is_active = question.is_active
    question.is_active = not is_active
    await sync_to_async(question.save)()
    if is_active:
        active_text = "So'rovnoma faol"
    else:
        active_text = "So'rovnoma nofaol"

    button.append([InlineKeyboardButton(text=active_text,callback_data=f"active_quiz:{question.pk}")])
    button.append([InlineKeyboardButton("So'rovnomani o'chirish",callback_data=f"delete_quiz:{question.pk}")])  
    button.append([InlineKeyboardButton(text="Ortga Qaytish",callback_data=f"quizes:{token}")]) 
    button.append([InlineKeyboardButton("So'rovnoma natijalarni yuklab olish",callback_data=f"download_quiz:{question.pk}")])
    await context.bot.delete_message(chat_id=chat_id,message_id=message_id)
    await context.bot.send_message(chat_id=chat_id,text=text,reply_markup=InlineKeyboardMarkup(button), parse_mode="HTML")

async def delete_quiz(update: Update, context: CallbackContext):

    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id

    question_id = update.callback_query.data.split(":")[1]
    question = await sync_to_async(Question.objects.get)(id=question_id)
    bot = await sync_to_async(lambda: question.bot)()
    token = bot.token
    button = []
    text = f"<b>So'rovnoma o'chirildi!!!</b>"
    options = await sync_to_async(list)(question.option.all())

    for option in options:
        await sync_to_async(option.delete)()
    await sync_to_async(question.delete)()
    

  
    button.append([InlineKeyboardButton(text="Ortga Qaytish",callback_data=f"quizes:{token}")]) 
    await context.bot.edit_message_text(chat_id=chat_id,text=text,reply_markup=InlineKeyboardMarkup(button), parse_mode="HTML",message_id=message_id)

async def download_quiz(update: Update, context: CallbackContext):

    chat_id = update.callback_query.message.chat_id
    question_id = update.callback_query.data.split(":")[1]
    question = await sync_to_async(Question.objects.get)(id=question_id)
    
    options = await sync_to_async(list)(question.option.all())

    survey_question = question.name
    total_counts = []
    voters = []
    for option in options:
        total_counts.append(f"jami = {option.total_vote}")
        voter = await sync_to_async(list)(option.votes.all())
        voter = [voter_item.first_name for voter_item in voter]
        voters.append(voter)
    filename = await sync_to_async(write_survey_results_to_csv)(survey_question,options,total_counts,voters)
    with open(filename, "rb") as file:
        await context.bot.send_document(chat_id=chat_id, document=file)
    import os 
    os.remove(filename)
    
async def delete_bot(update: Update, context: CallbackContext):

    data = update.callback_query.data.split(":")
    token = data[1]+":"+data[2]
    chat_id = update.callback_query.message.chat_id
    bot = await sync_to_async(Bot.objects.get)(token=token)

    message_id = update.callback_query.message.message_id

    bot_obj = bot1(token)
    await bot_obj.delete_webhook()
    await sync_to_async(bot.delete)()

    buttons = [
        [InlineKeyboardButton("Bosh Menyuga Qaytish",callback_data="main menu")],
        [InlineKeyboardButton("Ortga Qaytish",callback_data=f"Mening Botlarim")]
    ]

    await context.bot.edit_message_text(chat_id=chat_id,message_id=message_id,text="Bot O'chirildi",reply_markup=InlineKeyboardMarkup(buttons))


    
async def filter_callback_data(update: Update, context: CallbackContext):
    data = update.callback_query.data

    if data == "Mening Botlarim":
        await mybot(update=update, context=context)
    elif data == "back:start":
        await start(update=update, context=context)
    elif data == "main menu":
        await start(update=update, context=context)
    elif data == "Bot Yaratish":
        return await start_conversation(update, context)
    elif data == "cancel":
        await cancel(update, context)
    elif "cancel_quiz" in data.split(":"):
        await cancel_quiz(update, context)
    elif "bot" in data.split(":"):
        await select_bot(update, context)
    elif "quizes" in data.split(":"):
        await quizes(update,context)
    elif "channels" in data.split(":"):
        await bot_chanels_func(update,context)
    elif "select_quiz" in data.split(":"):
        await select_quiz(update,context)
    elif "active_quiz" in data.split(":"):
        await active_quiz(update,context)
    elif "delete_quiz" in data.split(":"):
        await delete_quiz(update,context)
    elif "download_quiz" in data.split(":"):
        await download_quiz(update,context)
    elif "delete_bot" in data.split(":"):
        await delete_bot(update,context)
    elif "create_quiz" in data.split(":"):
        return await start_conversation_quiz(update,context)
    elif "start_forward" in data.split(":"):
        return await start_forwrad(update,context)
    elif "cancel_forward" in data.split(":"):
        return await cancel_forward(update,context)
        

    