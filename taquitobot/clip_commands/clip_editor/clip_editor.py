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
import json
from tensorflow.keras.models import load_model
from clip_commands.clip_downloader.clip_downloader import download_outplayed_clip_from_discord_message

# =============================================================================
#
#                             Constant Declarations
#
# =============================================================================

FILE_PATH = os.path.abspath(__file__)
FOLDER_PATH = os.path.dirname(FILE_PATH)
MODEL_RELATIVE_PATH = 'neural_networks/taquitobot_clip_editor_crop2_NN.h5'
MODEL_PATH = os.path.join(FOLDER_PATH, MODEL_RELATIVE_PATH)

CROP_RIGHT = 1060
CROP_LEFT = 850
CROP_TOP = 775
CROP_BOTTOM = 970

SONG_FOLDER_RELATIVE_PATH = 'music/'
SONG_FOLDER_PATH = os.path.join(FOLDER_PATH, SONG_FOLDER_RELATIVE_PATH)

MP4_CODEC = "libx264"
CLIP_EDITOR_MODEL = load_model(MODEL_PATH, compile=False)

JSON_FILE_RELATIVE_PATH = 'clip_data.json'
JSON_FILE_PATH = os.path.join(FOLDER_PATH, JSON_FILE_RELATIVE_PATH)

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
        self.video_file, self.video_title, self.game_title = download_outplayed_clip_from_discord_message(
            discord_message)

        self.audio_track, self.audio_drop = get_random_audio_from_folder(
            SONG_FOLDER_PATH)

        # Generate moviepy video/audio clips objects
        self.audio_clip = moviepy.editor.AudioFileClip(SONG_FOLDER_PATH +
                                                       self.audio_track)
        self.video_clip = moviepy.editor.VideoFileClip(self.video_file)
        self.length_of_clip = self.video_clip.duration
        self.length_of_song = self.audio_clip.duration

        # Ensure that the song is long enough for the clip
        if self.length_of_song < self.length_of_clip:
            counter = 0
            while self.length_of_song < self.length_of_clip:
                self.audio_track, self.audio_drop = get_random_audio_from_folder(
            SONG_FOLDER_PATH)
                self.audio_clip = moviepy.editor.AudioFileClip(SONG_FOLDER_PATH +
                                                               self.audio_track)
                self.length_of_song = self.audio_clip.duration
                counter = counter + 1
                # if we try too many times abort getting song
                if counter == 100:
                    break

        # Generate moviepy video/audio clips objects
        self.audio_clip = moviepy.editor.AudioFileClip(SONG_FOLDER_PATH +
                                                       self.audio_track)

        # Get previous clip information
        with open(JSON_FILE_PATH, 'r') as clip_data:
            self.clip_data_from_file = json.load(clip_data)

    async def add_audio(self):
        """
        Function to add a random audio track to the clip and edit the video into a youtube short.
        """
        audio_start = self.audio_drop - await self.find_first_highlight()

        audio_subclip = self.audio_clip.subclip(
            audio_start, int(self.length_of_clip + audio_start))

        self.edited_video = self.video_clip.set_audio(audio_subclip)\
        
        # Convert the video to 16:9 aspect ratio (vertical)
        self.edited_video = self.edited_video.resize(height=960)
        centre = int(self.edited_video.w / 2)
        self.edited_video = self.edited_video.crop(x1=centre - 270, y1=0, x2=centre + 270, y2=960)
        
        # Remove the last 20% of the video (usually irrelevant)
        clip_duration = self.edited_video.duration 
        self.edited_video = self.edited_video.subclip(0, clip_duration)
        return None

    def save_video(self):
        """
        Function to save an edited video to the environment.
        :return: The video title and the path to the video.
        """
        try:
            self.new_filename = self.video_title + ' ' + self.game_title + '.mp4'
            self.edited_video.write_videofile(self.new_filename,
                                              fps=30,
                                              codec=MP4_CODEC,
                                              preset='superfast')

            with open(JSON_FILE_PATH, 'w') as clip_data:
                # Add the new video to completed videos
                self.clip_data_from_file["edited_videos"].append(
                    self.video_file)
                json.dump(self.clip_data_from_file, clip_data)

            self.delete_original_footage()
        except (NameError):
            print(
                'Video has not been edited yet, cannot save video that does not exist.'
            )

        return self.new_filename

    async def find_first_highlight(self):
        """
        Function to find the first highlight frame in the clip to sync up music with.
        :return: highlight_time: A float representing the time of the clip.
        """
        # This will loop to the length of the video in increments of 0.5
        for time_interval in [
                float(j) / 4 for j in range(0, 4 * int(self.length_of_clip), 1)
        ]:
            resized_clip = self.video_clip.crop(CROP_LEFT, CROP_TOP,
                                                CROP_RIGHT, CROP_BOTTOM)

            current_frame = resized_clip.get_frame(time_interval) / 255
            # Need to add one more dimension for the NN to take as input
            current_frame_aug = np.expand_dims(current_frame, axis=0)

            # prediction = 0 is no kill, 1 is kill
            prediction = CLIP_EDITOR_MODEL.predict(current_frame_aug)[0]

            if np.argmax(prediction) == 1:
                return time_interval
        return self.length_of_clip / 2

    def check_duplicate_video(self):
        """
        Function to check if the video has already been uploaded to prevent duplicates.
        :return: True if the video has been uploaded and False if this is the first occurance.
        """

        video_uploaded = False
        if self.video_file in self.clip_data_from_file["edited_videos"]:
            video_uploaded = True

        return video_uploaded
    
    def delete_original_footage(self):
        """
        Function to remove the original clip once video editing has finished.
        """
        print(f'video file is {self.video_file}')
        if os.path.exists(self.video_file):
            os.remove(self.video_file)
            print(f'Deleted {self.video_file}')


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

    # Get a unique song that was not used in the most recent edit
    song_path = random.choice(os.listdir(path))
    print(song_path)
    song_start_time = float(
        re.search(r'(\d+\$\d+)', song_path).group(1).replace('$', '.'))

    return song_path, song_start_time
