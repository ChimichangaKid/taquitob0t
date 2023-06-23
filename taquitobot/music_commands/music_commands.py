# =============================================================================
#
# Title: music_commands.py
#
# Author: Aidan
#
# Description: Script to send music related commands to the bot.
#
# =============================================================================

# =============================================================================
#
#                                     Imports
#
# =============================================================================

import discord
from discord.ext import commands
from music_commands.my_youtube.youtube_requests import fetch_song
from music_commands.my_youtube.youtube_exceptions import SongException
from music_commands.music_exceptions import JoinException

# =============================================================================
#
#                               Constant Declaration
#
# =============================================================================

FFMPEG_OPTIONS = {
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# =============================================================================
#
#                                     Classes
#
# =============================================================================


class MusicPlayer(commands.Cog):
    """
    Representation Invariant:
        title_list[i] == title of the song in song_queue[i]
        current_song == song playing on voice
    Abstraction Function:
        A MusicPlayer object is an object that abstractly represents a YouTube audio player in a Discord voice channel.
    """

    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.title_list = []
        self.song_queue = []
        self.current_song = ''

        self.voice = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("music_commands ready")

    # =============================================================================
    #
    #                                   Functions
    #
    # =============================================================================

    def play_next_song(self, ctx):
        """
        Helper function to play the next song in the queue, if there are no further songs remaining.
        :param: ctx: A discord.Context object, represents the context of the command being issued.
        :return: The title of the track that is currently playing.
        """
        if len(self.song_queue) > 0:
            self.is_playing = True

            song_url = self.song_queue.pop(0)
            song_title = self.title_list.pop(0)

            channel_id = ctx.channel.id
            channel = self.bot.get_channel(channel_id)

            # After the song has finished playing, send self.play_next_song
            self.voice.play(discord.FFmpegOpusAudio(song_url,
                                                    **FFMPEG_OPTIONS),
                            after=lambda x: self.play_next_song(ctx))
            self.bot.loop.create_task(
                channel.send(f"Playing song {song_title}"))
        else:
            self.is_playing = False

    async def queue_song(self, song_name: str) -> str:
        """
        Helper function to add the specified song to the queue after finding it from YouTube.
        :param: song_name: The name of the song that is being requested. Is in a string format
        :return: The title of the song that was fetched from YouTube.
        :raises: SongException if the song was not properly fetched from YouTube.
        """
        song_information = await fetch_song(song_name)
        if song_information:
            self.title_list.append(song_information['entries'][0]['title'])
            self.song_queue.append(song_information['entries'][0]['url'])
            return song_information['entries'][0]['title']
        else:
            raise SongException("Unable to fetch song from YouTube.")

    async def join_voice(self, ctx):
        """
        Helper function to attempt to join the voice channel of the user that issued a command.
        :param: ctx: The context of the command being sent. Should be of type discord.Context object.
        :raises: JoinException if the user issuing the command is not in a voice channel.
        """
        if self.voice is None:
            if ctx.author.voice:
                channel = ctx.message.author.voice.channel
                self.voice = await channel.connect()
            else:
                await ctx.send(
                    "Must be in a voice channel to use this command.")
                raise JoinException("Not in voice channel")
        else:
            channel = ctx.message.author.voice.channel
            self.voice = ctx.voice_client
            await ctx.voice_client.move_to(channel)

    # =============================================================================
    #
    #                                   Commands
    #
    # =============================================================================

    @commands.command(name="play", aliases=['p', 'P'])
    async def play(self, ctx):
        """
        Plays the requested video audio in a Discord call, if already playing a song add the requested song to a FIFI
        queue.
        :param: ctx: The context of the command being passed, contains detailed information about the request such as
                    message contents and user that issued the command.
        """

        song_name = ctx.message.content.split(None, 1)[1]

        try:
            await self.join_voice(ctx)
        except JoinException:
            await ctx.send(
                "Error joining voice channel. Check that you are in a channel before requesting."
            )
            return None

        try:
            queued_song = await self.queue_song(song_name)
            await ctx.send(f"Queued song {queued_song}.")
        except SongException:
            await ctx.send("Error fetching song from YouTube.")
            return None

        if not self.is_playing:
            self.play_next_song(ctx)

    @commands.command(name="leave", aliases=["disconnect", 'l', 'L'])
    async def leave(self, ctx):
        """
        Command to instruct the bot to disconnect from the voice channel. If not in a voice channel this command does
        nothing.
        :param: ctx: A discord.Context object, represents the context of the command being issued.
        """
        if ctx.voice_client:
            self.title_list.clear()
            self.song_queue.clear()
            await ctx.send(f"Disconnected from {ctx.voice_client}.")
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("Not in a voice channel...")

    @commands.command(name="pause")
    async def pause(self, ctx):
        """
        Command to pause the current song that is being played. If the current track is already paused then it will
        unpause the track.
        :param: ctx: A discord.Context object, represents the context of the command being issued.
        :raises: SongException if the track is not playing or paused.
        """

        if self.voice.is_playing():
            self.voice.pause()
            await ctx.send("Successfully paused.")
        elif self.voice.is_paused():
            self.voice.resume()
            await ctx.send("Successfully resumed.")
        else:
            await ctx.send("Unable to pause/resume")
            raise SongException("Unable to pause/resume.")

    @commands.command(name="skip", aliases=['s', 'S'])
    async def skip(self, ctx):
        """
        Command to skip the currently playing song and proceed to the next song in the queue.
        :param: ctx: A discord.Context object, represents the context of the command being issued.
        """

        if self.voice.is_playing() or self.voice.is_paused():
            self.voice.stop()
            await ctx.send(f"Skipped song {self.current_song}")

    @commands.command(name="queue", aliases=['q', 'Q'])
    async def queue(self, ctx):
        """
        Command to show the current songs in the queue. Displays the queue as a discord message.
        :param: ctx: A discord.Context object, represents the context of the command being issued.
        """

        if len(self.title_list) < 1:
            await ctx.send("No songs in queue.")
            return

        queue = "Queue: "

        for song_index, song_title in enumerate(self.title_list, start=1):
            queue = queue + "\n" + str(song_index) + '. ' + song_title

        await ctx.send("**" + queue + "**")

    @commands.command(name="remove", aliases=['r', 'R'])
    async def remove(self, ctx):
        """
        """
        index = ctx.message.content
        song_index = int(index.split(None, 1)[1]) - 1
        if -1 < song_index < len(self.song_queue):
            self.song_queue.pop(song_index)
            title = self.title_list.pop(song_index)
            await ctx.send("Removed: **" + str(song_index + 1) + '. ' + title + '**')
        else:
            await ctx.send("Invalid input brainless idjit")


async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))
