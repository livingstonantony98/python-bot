import os

from Crypto.SelfTest.Cipher.test_OFB import file_name
# importing necessary functions from dotenv library
from dotenv import load_dotenv

from Utils import Utils
from rooka.MegaUtils import MegaUtils
from scripts import mega_utils

# loading variables from .env file
load_dotenv()

API_KEY = os.getenv("KELLIE")
# API_KEY = os.getenv("ROOKA")
ROOKA_EMAIL = os.getenv("ROOKA_EMAIL")
ROOKA_PASSWORD = os.getenv("ROOKA_PASSWORD")

import os

from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, BotCommand
import datetime

from mega import Mega

mega = Mega()
m = mega.login(ROOKA_EMAIL, ROOKA_PASSWORD)

mega_utils = MegaUtils()
utils = Utils()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = ["hot_images","$Images"]
    # keyboard = [
    #     [KeyboardButton("Actress"), KeyboardButton("Button 2")],
    #     [KeyboardButton("Button 3")],
    #     [KeyboardButton("Button 4")]
    # ]
    keyboard = [[KeyboardButton(button)] for button in buttons]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await context.bot.set_my_commands([
        ('hot_image', 'Random Hot Image'),
    ])

    commands = [BotCommand("test", "to start something"), BotCommand("test2Z", "to stop something")]

    # await context.bot.set_my_commands(commands)

    # Button Feature
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Select an option:\n"
                                        "/hot_image",
                                   reply_markup=reply_markup)


async def random_pic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await utils.image_upload(update, context, mega_utils)


async def image_saver(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        folder_name = 'test_folder'

        message = await context.bot.send_message(chat_id=update.message.chat_id,
                                                 text=f'Uploading...', reply_to_message_id=update.message.message_id)
        file_name = f'{formatted_date}.jpg'
        img_path = f'{os.getcwd()}/leaked/images/{file_name}'
        caption = update.message.caption
        print(f'caption: {caption}')
        if caption == 'hot_images':
            folder_name = caption
        print(f'File saved successfully!: {file_name}, folder_name ${folder_name}')
        await (await context.bot.getFile(update.message.photo[-1].file_id)).download_to_drive(img_path)
        mega_utils = MegaUtils()
        # mega_utils.upload(img_path,'leaked')
        # mega_utils.upload(img_path, f'{folder_name}')
        print(f'File uploaded successfully!: {file_name}')

        if os.path.exists(img_path):
            os.remove(img_path)
            print(f'File removed successfully!: {file_name}')
        # await context.bot.send_message(chat_id=update.effective_chat.id,
        #                                text=f'Uploaded to: test_folder')
        await context.bot.edit_message_text(text=f'Uploaded to: {folder_name}', chat_id=message.chat_id,
                                            message_id=message.message_id)


    elif update.message.animation:
        file_id = update.message.animation.file_id
        file = await context.bot.get_file(file_id)
        file_name = f'{formatted_date}.gif'
        # print(f'File saved successfully!: {file_name}')
        # file_path = f'/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/gifs/{file_name}'
        # await (await context.bot.getFile(update.message.animation.file_id)).download_to_drive(file_path)


async def save_image_without_notifying_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %I-%M-%S-%f")[:-3] + " " + now.strftime("%p")
    if update.message.text:
        text = update.message.text
        username = update.message.from_user.username
        firstname = update.message.from_user.first_name
        lastname = update.message.from_user.last_name
        # phone_number = update.message.contact.phone_number
        print(f'username: {username}, name: {firstname} {lastname}, text: {text}')

    if update.message.photo:
        folder_name = 'test_folder'

        file_name = f'{formatted_date}.jpg'
        img_path = f'{os.getcwd()}/leaked/images/{file_name}'
        caption = update.message.caption
        print(f'caption: {caption}')
        # if caption=='hot_images':
        #     folder_name=caption
        print(f'File saved successfully!: {file_name}, folder_name ${folder_name}')
        await (await context.bot.getFile(update.message.photo[-1].file_id)).download_to_drive(img_path)
        mega_utils = MegaUtils()
        # mega_utils.upload(img_path,'leaked')
        # mega_utils.upload(img_path, f'{folder_name}')
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


async def hot_images(update, context):
    await utils.get_random_pic(update, context, mega_utils)


app = ApplicationBuilder().token(API_KEY).build()

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)
hot_image_handler = CommandHandler('hot_image', hot_images)

app.add_handler(start_handler)
app.add_handler(help_handler)
app.add_handler(hot_image_handler)

# app.add_handler(MessageHandler(filters=None, callback=image_saver)) # upload images
# app.add_handler(MessageHandler(filters=None, callback=save_image_without_notifying_user)) # upload images
app.add_handler(MessageHandler(filters=None, callback=random_pic))
# app.add_handler(message_handler)
app.run_polling()
