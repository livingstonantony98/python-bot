from fileinput import filename

from mega import Mega
import os
from dotenv import load_dotenv


class MegaUtils:
    load_dotenv()

    API_KEY = os.getenv("ROOKA")
    ROOKA_EMAIL = os.getenv("ROOKA_EMAIL")
    ROOKA_PASSWORD = os.getenv("ROOKA_PASSWORD")

    mega = Mega()
    m = mega.login(ROOKA_EMAIL, ROOKA_PASSWORD)

    def upload(self, file_path, folder):
        if not self.is_folder_exist(folder):  # Check folder is a folder exist otherwise create
            self.create_folder(folder)
        folder = self.m.find(folder)
        self.m.upload(filename=file_path, dest=folder[0])

    def details(self):
        files = self.m.get_files()
        for f in files:
            filename = files[f]['a']['n']

            print(files[f])

            if files[f]['t'] == 0:
                print(filename)
                print(self.m.get_link(self.m.find(filename)))
            else:
                print('Dir: ' + filename)

    # Create a folder
    def create_folder(self, folder_name):
        if not self.is_folder_exist(folder_name):
            self.m.create_folder(folder_name)
            print(f"Folder created successfully: {folder_name}")
        else:
            print(f"Folder already exist: {folder_name}")

    def is_folder_exist(self, folder_name):
        return self.m.find(folder_name) is not None

    def get_list_of_folders(self):
        self.m.get_files()
