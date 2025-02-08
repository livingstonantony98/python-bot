# import os
# # importing necessary functions from dotenv library
# from dotenv import load_dotenv, dotenv_values
# # loading variables from .env file
# load_dotenv()
#
# print(os.getenv("MY_KEY"))
#
# from mega import Mega
#
# mega = Mega()
# # m = mega.login(os.getenv("MEGA_USERNAME"), os.getenv("MEGA_PASSWORD"))
# m = mega.login(os.getenv("ROOKA_USERNAME"), os.getenv("ROOKA_PASSWORD"))
# filename = "/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/leaked/images/2024-12-22 051053479 PM.jpg"
# folder = m.find('leaked')
# m.upload(filename=filename, dest=folder[0])
# files = m.get_files()
# for f in files:
# 	filename = files[f]['a']['n']
#
# 	print(files[f])
#
# 	if files[f]['t']==0:
# 		print(filename)
# 		print(m.get_link(m.find(filename)))
# 	else:
# 		print('Dir: '+filename)
from rooka.MegaUtils import MegaUtils

mega_utils = MegaUtils()

# mega_utils.upload(file_path="/Users/apple/Downloads/Learning Projects/Python/TelegramBot/TelegramBot/images/f7a97912-f861-4aa9-ae15-bb3b56f72309.jpg",folder='leaked2')

# print(mega_utils.is_folder_exist('tamana2'))

mega_utils.get_list_of_folders()