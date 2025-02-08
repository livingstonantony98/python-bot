import os

# importing necessary functions from dotenv library
from dotenv import load_dotenv

from rooka.MegaUtils import MegaUtils

# loading variables from .env file
load_dotenv()

API_KEY = os.getenv("ROOKA")
ROOKA_EMAIL =  os.getenv("ROOKA_EMAIL")
ROOKA_PASSWORD =  os.getenv("ROOKA_PASSWORD")

import os

from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler
from telegram import Update
import datetime

from mega import Mega

mega = Mega()
m = mega.login(ROOKA_EMAIL, ROOKA_PASSWORD)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # if update.message.new_chat_members:
        # await update.message.reply_text("Image downloaded successfully!")
    now = datetime.datetime.now()
    formatted_date =now.strftime("%Y-%m-%d %I-%M-%S-%f")[:-3] + " " + now.strftime("%p")
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
        mega_utils.upload(img_path,'leaked')
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


app = ApplicationBuilder().token(API_KEY).build()
app.add_handler(MessageHandler(filters=None, callback=handle_message))
app.run_polling()

