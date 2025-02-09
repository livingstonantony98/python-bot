import os

from Crypto.SelfTest.Cipher.test_OFB import file_name
# importing necessary functions from dotenv library
from dotenv import load_dotenv

from rooka.MegaUtils import MegaUtils
from scripts import mega_utils

# loading variables from .env file
load_dotenv()

API_KEY = os.getenv("KELLIE")
ROOKA_EMAIL = os.getenv("ROOKA_EMAIL")
ROOKA_PASSWORD = os.getenv("ROOKA_PASSWORD")

import os

from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
import datetime

from mega import Mega

mega = Mega()
m = mega.login(ROOKA_EMAIL, ROOKA_PASSWORD)

mega_utils = MegaUtils()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = ["hot_images"]
    # keyboard = [
    #     [KeyboardButton("Actress"), KeyboardButton("Button 2")],
    #     [KeyboardButton("Button 3")],
    #     [KeyboardButton("Button 4")]
    # ]
    keyboard = [[KeyboardButton(button)] for button in buttons]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Select an option:",
                                   reply_markup=reply_markup)


async def random_pic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %I-%M-%S-%f")[:-3] + " " + now.strftime("%p")

    text = update.message.text
    if update.message.text:
        text = update.message.text
        username = update.message.from_user.username
        firstname = update.message.from_user.first_name
        lastname = update.message.from_user.last_name
        # phone_number = update.message.contact.phone_number
        # print(f'username: {username}, name: {firstname} {lastname}, text: {text}')

    if update.message.photo:
        img_path = f'{os.getcwd()}/images/{formatted_date}.jpg'
        caption = update.message.caption
        print(f'caption: {caption}')
        await (await context.bot.getFile(update.message.photo[-1].file_id)).download_to_drive(img_path)
        # await update.message.reply_text("Image downloaded successfully!")
    if text == "hot_images":
        # await update.message.reply_text(text="You selected Button 1!")

        file_name, url = mega_utils.get_random_image_from("hot_images")
        mega_utils.download(url)
        # await update.message.reply_photo(photo="/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/images/test_image.jpeg")
        file_path = f"/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/leaked/images/${file_name}"
        await update.message.reply_photo(
            photo=file_path)
        # await update.message.reply_photo(
        #     photo="/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/leaked/images/20250208_170113.jpg")

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'File removed successfully!: {file_name}')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # if update.message.new_chat_members:
    # await update.message.reply_text("Image downloaded successfully!")
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %I-%M-%S-%f")[:-3] + " " + now.strftime("%p")
    # print(f'message type: {update}')
    if update.message.text:
        text = update.message.text
        username = update.message.from_user.username
        firstname = update.message.from_user.first_name
        lastname = update.message.from_user.last_name
        # phone_number = update.message.contact.phone_number
        print(f'username: {username}, name: {firstname} {lastname}, text: {text}')

    if update.message.photo:
        file_name = f'{formatted_date}.jpg'
        img_path = f'{os.getcwd()}/leaked/images/{file_name}'
        caption = update.message.caption
        print(f'caption: {caption}')
        print(f'File saved successfully!: {file_name}')
        await (await context.bot.getFile(update.message.photo[-1].file_id)).download_to_drive(img_path)
        mega_utils = MegaUtils()
        # mega_utils.upload(img_path,'leaked')
        mega_utils.upload(img_path, 'test_folder')
        print(f'File uploaded successfully!: {file_name}')

        if os.path.exists(img_path):
            os.remove(img_path)
            print(f'File removed successfully!: {file_name}')

    elif update.message.animation:
        file_id = update.message.animation.file_id
        file = await context.bot.get_file(file_id)
        file_name = f'{formatted_date}.gif'
        # print(f'File saved successfully!: {file_name}')
        # file_path = f'/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/gifs/{file_name}'
        # await (await context.bot.getFile(update.message.animation.file_id)).download_to_drive(file_path)


async def help_command(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='I can understand /start and /help commands.')


app = ApplicationBuilder().token(API_KEY).build()

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)

message_handler = MessageHandler(filters=None, callback=handle_message)

app.add_handler(start_handler)
app.add_handler(help_handler)
app.add_handler(MessageHandler(filters=None, callback=random_pic))
# app.add_handler(message_handler)
app.run_polling()
