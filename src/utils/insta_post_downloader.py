import re
from typing import Tuple, List

import instaloader
import argparse
import requests
from tqdm import tqdm
from datetime import datetime
import os


# if post.is_video is True then it will be url of video file
class InstaPostDownloader:
    def get_instagram_post(self, post_url: str) -> Tuple[List[str], List[str]]:
        """
        Get an Instagram post using the instaloader library.

        Args:
            post_url (str): The URL of the Instagram post.

        Returns:
            instaloader.Post: The Instagram post object.
        """
        # post_url = post_url.split('?')[0]  # Remove query parameters

        # print(file_paths)

        try:
            L = instaloader.Instaloader()
            post_shortcode = re.search(r'(p|reel)/([^/?]+)/?', post_url).group(2)
            print(post_shortcode)
            post = instaloader.Post.from_shortcode(L.context, post_shortcode)

            current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S") + str(datetime.now().microsecond // 1000)
            folder_path = f"{current_datetime}_folder"
            L.download_post(post, folder_path)

            # Initialize an empty list to store the file paths

            jpg_files = list(map(lambda filename: os.path.abspath(os.path.join(folder_path, filename)),
                                 filter(lambda filename: filename.endswith('.jpg'),
                                        os.listdir(folder_path))))

            mp4_files = list(map(lambda filename: os.path.abspath(os.path.join(folder_path, filename)),
                                 filter(lambda filename: filename.endswith('.mp4'),
                                        os.listdir(folder_path))))
            return jpg_files, mp4_files
        except BaseException as e:
            print(e)
            return [], []

    # ... (rest of the code remains the same)


if __name__ == '__main__':
    # InstaPostDownloader().post("https://www.instagram.com/p/DFuViBIybVG/")
    InstaPostDownloader().get_instagram_post("https://www.instagram.com/reel/DGLIZhDzlyR")
