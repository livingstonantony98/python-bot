import re
import instaloader
import argparse
import requests
from tqdm import tqdm
from datetime import datetime


# if post.is_video is True then it will be url of video file

def get_instagram_post(post_url):
    """
    Get an Instagram post using the instaloader library.

    Args:
        post_url (str): The URL of the Instagram post.

    Returns:
        instaloader.Post: The Instagram post object.
    """
    # post_url = post_url.split('?')[0]  # Remove query parameters
    L = instaloader.Instaloader()
    post_shortcode = re.search(r'(p|reel)/([^/?]+)/?', post_url).group(2)
    print(post_shortcode)
    post = instaloader.Post.from_shortcode(L.context, post_shortcode)

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S") + str(datetime.now().microsecond // 1000)
    L.download_post(post,f"{current_datetime}_folder")
    return post


def download_file(url, filename):
    """
    Download a file from a given URL and save it to a local file.

    Args:
        url (str): The URL of the file to download.
        filename (str): The local filename to save the file as.

    Returns:
        None
    """
    # Send a GET request to the URL
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to download file. Status code: {response.status_code}")
        return

    # Get the total size of the file
    total_size = int(response.headers.get('content-length', 0))

    # Create a progress bar
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    # Open the local file in write binary mode
    with open(filename, 'wb') as file:
        # Iterate over the response content in chunks
        for chunk in response.iter_content(chunk_size=1024):
            # Write the chunk to the local file
            file.write(chunk)

            # Update the progress bar
            progress_bar.update(len(chunk))

    # Close the progress bar
    progress_bar.close()


# ... (rest of the code remains the same)

def main():
    parser = argparse.ArgumentParser(description='Instagram Post Downloader')
    parser.add_argument('--url', help='URL of the Instagram post')
    args = parser.parse_args()

    if not args.url:
        print("Please provide the URL of the Instagram post")
        return

    post_url = args.url
    post = get_instagram_post(post_url)
    # photo_url = post.url  # this will be post's thumbnail (or first slide)
    # video_url = post.video_url
    #
    # current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S") + str(datetime.now().microsecond // 1000)
    #
    # if photo_url:
    #     filename = f"{current_datetime}_photo.jpg"
    #     download_file(photo_url, filename)
    #     print(f"Photo downloaded successfully: {filename}")
    # if video_url:
    #     filename = f"{current_datetime}_video.mp4"
    #     download_file(video_url, filename)
    #     print(f"Video downloaded successfully: {filename}")


if __name__ == '__main__':
    main()
