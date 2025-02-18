import requests
from tqdm import tqdm


class FileDownloader:
    def download_file(self, url, filename):
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
