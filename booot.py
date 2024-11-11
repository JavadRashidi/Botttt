from pyrogram import Client, filters
from pyrogram.types import *
from pyromod import listen
import logging
from dbt import Database
from datetime import datetime, timedelta
import asyncio

bot = Client(
    'reminder',
    api_id=27213097,
    api_hash="f9f95e00a37c78bc4e63691c464157c0",
    bot_token="7883384618:AAHvpATe04ph15_lhmQNQbS6JzyE84IpVvY"
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

Admin = 540350821
user_states = {}

########## Panel Admin ##########
@bot.on_message(filters.private & filters.user(Admin))
async def Panel_admin(client, message):
    chat_id = message.chat.id
    text = message.text
    dbt = Database()
    mark2 = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton("تعداد کاربران")
        ],
        [
            KeyboardButton("پیام همگانی"),
            KeyboardButton("پیام تکی")
        ],
        [
            KeyboardButton("بلاک کردن"),
            KeyboardButton("آزاد کردن")
        ]
    ], resize_keyboard=True)

    if text == "/start":
        await bot.send_message(chat_id, "سلام ادمین عزیز", reply_markup=mark2)
    elif text == "تعداد کاربران":
        users = dbt.all_user()
        await message.reply(f"تعداد کاربران ربات {len(users)}")
    elif text == "پیام همگانی":
        update = await bot.ask(chat_id, "پیام خود را ارسال کنید")
        users = dbt.all_user()
        succ = err = 0

        for pv in users:
            try:
                await bot.send_message(pv, update.text)
                succ += 1
            except:
                err += 1

        await message.reply(f""" 
تعداد کاربران ربات: {len(users)}
ارسال شده‌ها: {succ}
ارسال نشده‌ها: {err}""")
    elif text == "پیام تکی":
        user_id = await bot.ask(chat_id, "آیدی شخص مورد نظر را وارد کنید")
        message_text = await bot.ask(chat_id, "پیام خود را ارسال کنید ")
        try:
            await bot.send_message(int(user_id.text), message_text.text)
            await message.reply("پیام با موفقیت ارسال شد")
        except Exception as e:
            await message.reply(f"پیام ارسال نشده: {e}\nمطمئن شوید کاربر از قبل ربات را استارت کرده است")
    elif text == "بلاک کردن":
        update_id = await bot.ask(chat_id, "آیدی فرد مورد نظر را ارسال کنید")
        if dbt.add_block(update_id.text):
            await message.reply("کاربر با موفقیت بلاک شد")
            await bot.send_message(update_id.text, "شما توسط ادمین بلاک شدید")
        else:
            await message.reply("کاربر بلاک نشد")
    elif text == "آزاد کردن":
        update_id = await bot.ask(chat_id, "آیدی فرد مورد نظر را ارسال کنید")
        if dbt.remove_block(update_id.text):
            await message.reply("کاربر با موفقیت آزاد شد")
            await bot.send_message(update_id.text, "شما توسط ادمین آنبلاک شدید")
        else:
            await message.reply("کاربر آزاد نشد")
    

########## Start ##########
async def Start(client, message):
    chat_id = message.chat.id
    users = message.chat.first_name
    mark = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton("یادآوری 📆"),
        ],
        [
            KeyboardButton("👈🏻 زیر مجموعه گیری 👉🏻"),
            KeyboardButton("VIP"),
            KeyboardButton("درباره ربات 🤖")
        ],
        [
            KeyboardButton("پشتیبانی 📞")
        ]
    ], resize_keyboard=True)
    await bot.send_message(chat_id, f"سلام {users} به ربات یاد آور خوش آمدید🌹", reply_markup=mark)

########## Reminder ##########
async def Reminder(client, message):
    chat_id = message.chat.id
    mark2 = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("یاد آوری روزانه 🗒", callback_data="daily_reminder"),
            InlineKeyboardButton("لیست یاد آوری های من 📃", callback_data="list")
        ]
    ])
    await bot.send_message(chat_id, "👇🏻 یکی از گزینه‌های زیر را انتخاب", reply_markup=mark2)

@bot.on_callback_query(filters.regex("daily_reminder"))
async def daily_reminder_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    await bot.send_message(chat_id, "لطفاً یادآوری روزانه خود را وارد کنید.")

@bot.on_callback_query(filters.regex("list"))
async def list_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    dbt = Database()
    reminders = dbt.get_reminders(chat_id)
    task_list = "\n".join([f"{reminder[0]} در ساعت {reminder[1].strftime('%H:%M')}" for reminder in reminders])
    if task_list:
        await bot.send_message(chat_id, f"یادآوری‌های شما:\n{task_list}")
    else:
        await bot.send_message(chat_id, "هیچ یادآوری تنظیم نشده است.")
    

########## Link ##########
async def Link(client, message):
    chat_id = message.chat.id
    user = message.chat.first_name
    await bot.send_message(chat_id, f"""
   لینک از طرف {user}

    https://telegram.me/reminderme2024_bot?start={chat_id}
""")

########## VIP ##########
async def VIP(client, message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "پیام خود را وارد کنید ")

########## About bot ##########
async def About_bot(client, message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "پیام خود را وارد کنید ")

########## Support ##########
async def Support(client, message):
    chat_id = message.chat.id

    message_support = await bot.ask(chat_id, "پیام خود را به ربات ارسال کنید")
    await bot.send_message(chat_id, "پیام با موفقیت به مدیریت ارسال شد ")

    try:
        await bot.send_message(Admin, f"شما یک پیام جدید دارید:\nآیدی عددی:{message_support.from_user.id}\n\n{message_support.text}")
    except Exception as ee:
        print(ee)

########## Main ##########
@bot.on_message()
async def Main(client, message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id

    dbt = Database()
    dbt.add_user(user_id)
    if dbt.check_block(user_id):
        return

    if text == "/start":
        await Start(client, message)

    elif text.startswith("/start "):
        user_chat_friend = text.replace("/start ", "")
        if dbt.update_user(user_id, user_chat_friend):
            await bot.send_message(user_chat_friend, "یک نفر با لینک شما به ربات دعوت شد")
        else:
            await bot.send_message(user_chat_friend, "قبلاً با لینک شما اد شده است")
        await Start(client, message)
    elif text == "یادآوری 📆" or text == "/reminder":
        await Reminder(client, message)
    elif text == "👈🏻 زیر مجموعه گیری 👉🏻" or text == "/link":
        await Link(client, message)
    elif text == "VIP" or text == "/vip":
        await VIP(client, message)
    elif text == "درباره ربات 🤖" or text == "/about":
        await About_bot(client, message)
    elif text == "پشتیبانی 📞" or text == "/support":
        await Support(client, message)

    

########## Check Reminders ##########
async def check_reminders():
    dbt = Database()
    while True:
        now = datetime.now()
        reminders = dbt.get_due_reminders()
        for reminder in reminders:
            id, chat_id, text, remind_time = reminder
            await bot.send_message(chat_id, f"یادآوری: {text}")
            dbt.delete_reminder(id)
        await asyncio.sleep(10)
    

bot.start()
loop = asyncio.get_event_loop()
loop.create_task(check_reminders())
loop.run_forever()

