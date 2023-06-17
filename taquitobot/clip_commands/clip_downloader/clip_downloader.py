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
import re
from bs4 import BeautifulSoup

# =============================================================================
#
#                               Constant Declaration
#
# =============================================================================

OUTPLAYED_PATTERN = r"https://outplayed\.tv/media/.*"


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
    :return: video_file: The filename of the video that was downloaded.
    """
    # Gets the end of the url (only the mp4 part
    video_file = os.path.basename(video_link)

    r = requests.get(video_link)

    with open(video_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    return video_file


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


def download_outplayed_clip_from_discord_message(discord_message):
    """
    Function that takes a discord message containing outplayed.tv clip and downloads
    the clip to the local environment as an mp4 file.
    :param: discord_message: The discord message as string containing the outplayed.tv link.
    :return: video_file: The videofile title that was downloaded at the root of the repository.
    :return: video_title: The rest of the discord message to be used as a title.
    """
    # Get the outplayed link from the message
    try:
        outplayed_url = re.search(OUTPLAYED_PATTERN, discord_message).group()
    except:
        print("Error has occurred in finding link")
        return None

    video_file = download_video(extract_video_link(outplayed_url))

    # Get vido title from rest of message
    video_title = re.sub(OUTPLAYED_PATTERN, "", discord_message, re.IGNORECASE)

    return video_file, video_title
