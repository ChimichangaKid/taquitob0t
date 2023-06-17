# =============================================================================
#
# Title: clip_editor.py
#
# Author: Aidan
#
# Description: Script to edit videos downloaded to the environment.
#
# =============================================================================

# =============================================================================
#
#                                   Imports
#
# =============================================================================

import moviepy.editor
import os
import random
from clip_commands.clip_downloader.clip_downloader import download_outplayed_clip_from_discord_message

# =============================================================================
#
#                             Constant Declarations
#
# =============================================================================

SONG_FOLDER_PATH = 'taquitobot/clip_commands/clip_editor/music/'
MP4_CODEC = "libx264"


# =============================================================================
#
#                                   Classes
#
# =============================================================================

class ClipEditor:

    def __init__(self, discord_message):
        """
        Creates a clip editor to assist in editing the video, takes a discord message as argument.
        :param: discord_message: The discord message as a string containing the outplayed.tv clip link.
        """
        self.video_file, self.video_title = download_outplayed_clip_from_discord_message(discord_message)
        self.audio_track = get_random_audio_from_folder(SONG_FOLDER_PATH)

        # Generate moviepy video/audio clips objects
        self.audio_clip = moviepy.editor.AudioFileClip(SONG_FOLDER_PATH + self.audio_track)
        self.video_clip = moviepy.editor.VideoFileClip(self.video_file)
        self.edited_video = None

    async def add_audio(self):
        """
        Function to add a random audio track to the clip.
        """
        audio_start = 5  # arbitrary start time
        length_of_audio = self.video_clip.duration
        audio_subclip = self.audio_clip.subclip(audio_start, int(length_of_audio + audio_start))

        self.edited_video = self.video_clip.set_audio(audio_subclip)

        return None

    def save_video(self):
        """
        Function to save an edited video to the environment.
        """
        try:
            self.edited_video.write_videofile(self.video_title + 'edited.mp4', fps=30, codec=MP4_CODEC,
                                              preset='superfast')
        except NameError:
            print('Video has not been edited yet, cannot save video that does not exist.')

        return None


# =============================================================================
#
#                                   Functions
#
# =============================================================================

def get_random_audio_from_folder(path):
    """
    Helper function to generate a random song from a folder of songs.
    :param: path: path to the folder to randomly select a file.
    :returns: The title of the file that was chosen.
    """

    return random.choice(os.listdir(path))
