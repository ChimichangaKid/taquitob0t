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
import numpy as np
import random
import re
# IMPORTANT TO IMPORT TENSORFLOW 2.9.3 ON REPLIT FREE, OTHERWISE THERE IS NOT ENOUGH SPACE
from tensorflow.keras.models import load_model
from clip_commands.clip_downloader.clip_downloader import download_outplayed_clip_from_discord_message

# =============================================================================
#
#                             Constant Declarations
#
# =============================================================================

CROP_RIGHT = 1060
CROP_LEFT = 850
CROP_TOP = 775
CROP_BOTTOM = 970

SONG_FOLDER_PATH = 'taquitobot/clip_commands/clip_editor/music/'
MP4_CODEC = "libx264"
CLIP_EDITOR_MODEL = load_model(
    'taquitobot/clip_commands/clip_editor/neural_networks/taquitobot_clip_editor_crop2_NN.h5',
    compile=False)


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
        self.video_file, self.video_title = download_outplayed_clip_from_discord_message(
            discord_message)
        self.audio_track, self.audio_drop = get_random_audio_from_folder(SONG_FOLDER_PATH)

        # Generate moviepy video/audio clips objects
        self.audio_clip = moviepy.editor.AudioFileClip(SONG_FOLDER_PATH +
                                                       self.audio_track)
        self.video_clip = moviepy.editor.VideoFileClip(self.video_file)
        self.length_of_clip = self.video_clip.duration

    async def add_audio(self):
        """
        Function to add a random audio track to the clip.
        """
        audio_start = self.audio_drop - await self.find_first_highlight()

        audio_subclip = self.audio_clip.subclip(
            audio_start, int(self.length_of_clip + audio_start))

        self.edited_video = self.video_clip.set_audio(audio_subclip)

        return None

    def save_video(self):
        """
        Function to save an edited video to the environment.
        """
        try:
            self.edited_video.write_videofile(self.video_title + 'edited.mp4',
                                              fps=30,
                                              codec=MP4_CODEC,
                                              preset='superfast')
        except (NameError):
            print(
                'Video has not been edited yet, cannot save video that does not exist.'
            )

        return None

    async def find_first_highlight(self):
        """
        Function to find the first highlight frame in the clip to sync up music with.
        :return: highlight_time: A float representing the time of the clip.
        """
        # This will loop to the length of the video in increments of 0.5
        for time_interval in [
            float(j) / 4 for j in range(0, 4 * int(self.length_of_clip), 1)
        ]:
            # resize video
            # resized_clip = self.video_clip.resize(height=135, width=240)
            resized_clip = self.video_clip.crop(CROP_LEFT, CROP_TOP, CROP_RIGHT, CROP_BOTTOM)

            current_frame = resized_clip.get_frame(time_interval) / 255
            # Need to add one more dimension for the NN to take as input
            current_frame_aug = np.expand_dims(current_frame, axis=0)

            # prediction = 0 is no kill, 1 is kill
            prediction = CLIP_EDITOR_MODEL.predict(current_frame_aug)[0]

            if np.argmax(prediction) == 1:
                return time_interval
        return self.length_of_clip / 2


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

    song_path = random.choice(os.listdir(path))

    # Regex gets the first digits of the filename which contain the song beat drop timing
    song_start_time = int(re.match(r'^(\d+)', song_path).group(1))

    return song_path, song_start_time
