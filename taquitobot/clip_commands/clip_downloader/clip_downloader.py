# =============================================================================
#
# Title: clip_downloader.py
#
# Author: Aidan
#
# Description: Script to download videos from outplayed.tv.
#
# =============================================================================

# =============================================================================
#
#                                   Imports
#
# =============================================================================

import requests
import os
from bs4 import BeautifulSoup


# =============================================================================
#
#                                   Functions
#
# =============================================================================

# Source: https://stackoverflow.com/questions/30953104/download-video-from-url-in-python
def download_video(video_link):
    """
    Helper function to download a video from the specified link.
    :param: video_link: A url link in string format to the video to be downloaded.
    """
    # Gets the end of the url (only the mp4 part
    video_file = os.path.basename(video_link)

    r = requests.get(video_link)

    with open(video_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    return None


def extract_video_link(url):
    """
    Helper function to convert the outplayed link to the raw .mp4 link.
    :param: url: The url of the outplayed clip that was posted in the discord
    :return: mp4_link: The string link to the mp4 file to be downloaded
    """
    url_string = requests.get(url)
    html = url_string.text

    soup = BeautifulSoup(html, 'html.parser')
    video_tag = soup.find('video')
    mp4_link = video_tag['src']

    return mp4_link
