# =============================================================================
#
# Title: youtube_requests.py
#
# Author: Aidan
#
# Description: Script to interface with YouTube related commands.
#
# =============================================================================

# =============================================================================
#
#                                   Imports
#
# =============================================================================
import yt_dlp
from music_commands.my_youtube.youtube_exceptions import SongException

# =============================================================================
#
#                             Constant Declarations
#
# =============================================================================

ydl_opts = {
    'format':
    'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


# =============================================================================
#
#                                   Functions
#
# =============================================================================
async def fetch_song(song_name: str) -> dict:
    """
    Helper function to obtain information about the requested song from YouTube.
    :param song_name: The name of the song that is being requested.
    :return: A dict that contains information about the requested song, importantly the url and
             name of the song.
    :raises: SongException if the specified song was not fetched from YouTube.
    """
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            song_information = ydl.extract_info(f"ytsearch:{song_name}",
                                                download=False)
            return song_information
    except Exception:
        raise SongException("Error occurred fetching song from YouTube.")
