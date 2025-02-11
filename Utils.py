import datetime

from telegram import Update
from telegram.ext import ContextTypes
import os

from rooka.MegaUtils import MegaUtils


class Utils:
    async def image_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE, mega_utils: MegaUtils):
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
            await self.get_random_pic(update, context, mega_utils, text)
        # elif text == "$Images":
        #     await self.get_random_pic(update, context, mega_utils, "Images")

    async def get_random_pic(self, update: Update, context: ContextTypes.DEFAULT_TYPE, mega_utils: MegaUtils,
                             folder_name="hot_images"):

        message = await context.bot.send_message(chat_id=update.message.chat_id,
                                                 text=f'Loading...')
        file_name, url = mega_utils.get_random_image_from(folder_name)
        mega_utils.download(url)
        # await update.message.reply_photo(photo="/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/images/test_image.jpeg")
        file_path = f"/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/leaked/images/{file_name}"
        print(f"File: {file_path}")
        await context.bot.send_photo(
            photo=file_path, chat_id=update.effective_chat.id)
        await context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)

        # await update.message.reply_photo(
        #     photo="/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/leaked/images/20250208_170113.jpg")

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'File removed successfully!: {file_name}')
