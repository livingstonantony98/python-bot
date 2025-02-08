import datetime
import glob
# loading variables from .env file
import os
from random import randrange

# importing necessary functions from dotenv library
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler

load_dotenv()
API_KEY = os.getenv("KELLIE")
FOLDER="images"


# Enter File/Folder Name
from mega import Mega

mega = Mega()
m = mega.login(email, password)
filename = "data.csv"
m.upload(filename)



async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Actress"), KeyboardButton("Button 2")],
        [KeyboardButton("Button 3")]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                      text="Select an option:",
                                      reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:


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
    if text == "Actress":
        # await update.message.reply_text(text="You selected Button 1!")
        images = glob.glob(f'{os.getcwd()}/images/*.jpg')
        image = images[randrange(len(images))]
        print(image)
        # await update.message.reply_photo(photo="/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/images/test_image.jpeg")
        await update.message.reply_photo(photo=image)
    # elif text == "Button 2":
    #     await update.message.reply_text("You selected Button 2!")
    # elif text == "Button 3":
    #     await update.message.reply_text("You selected Button 3!")
    # else:
    #     await update.message.reply_text("Invalid option. Please select again.")

app = ApplicationBuilder().token(API_KEY).build()

# app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters=None, callback=handle_message))

app.run_polling()