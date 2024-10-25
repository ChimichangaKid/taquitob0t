"""
music_commands.py

File that handles commands related to requesting music to be played over the 
bot. Has class definitions for the cog and interfaces with yt_dlp.

Attributes:
    FFMPEG_OPTIONS (dict): Dictionary of options for FFMPEG audio processing.

TODO:
    - Modularize the code, try and integrate youtube methods and exceptions 
    better so the code is more organized and less spread out.

Versioning:
    Author: Aidan (Chimichanga Kid)
    Date: 2024-07-21
    Version: 1.2.2

Notes:
    Private methods and variables are documented to assist developers that need
    to understand the underlying code. 
"""
import discord
from discord.ext import commands
from music_commands.my_youtube.youtube_requests import fetch_song
from music_commands.my_youtube.youtube_exceptions import SongException
from music_commands.music_exceptions import JoinException

FFMPEG_OPTIONS = {
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


class MusicPlayer(commands.Cog):
    """
    Class to handle information about the music playing on the bot and getting
    music from YouTube.

    Args:
        bot (discord.ext.bot): The bot object to connect the commands to.
    
    Attributes:

    """

    """
    Private Attributes:
        _bot (discord.ext.bot): Bot object to connect the commands to.
        _is_playing (bool): Boolean if the bot is currently playing music.
        _title_list (array): Array of strings representing the titles FIFO.
        _song_queue (array): Array of links to the song on YouTube matching 
            with _title_list FIFO.
        _current_song (str): String that is the song title of the song 
            currently playing on the bot.
        _voice (discord.VoiceClient): VoiceClient object that contains 
            information about the voice channel that is requesting songs.
    """
    def __init__(self, bot):
        self._bot = bot

        self._is_playing = False
        self._title_list = []
        self._song_queue = []
        self._current_song = ''

        self._voice = None

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Method to inform the user when the music command cogs have been 
        properly loaded.
        """
        print("music_commands ready")

    @commands.command(name="play", aliases=['p', 'P'])
    async def play(self, ctx):
        """
        Command that plays the requested video audio in a Discord call, 
        if already playing a song add the requested song to a FIFO queue.
        
        Args:
            ctx (discord.ext.commands.Context): Discord Context object 
                containing information about the command request.
        
        Raises:
            JoinException (Exception): If the bot is unable to join the channel
                successfully.
        """

        song_name = ctx.message.content.split(None, 1)[1]

        try:
            await self._join_voice(ctx)
        except JoinException:
            await ctx.send(
                """Error joining voice channel. Check that you are in a channel
                before requesting."""
            )
            return None

        try:
            queued_song = await self._queue_song(song_name)
            await ctx.send(f"Queued song {queued_song}.")
        except SongException:
            await ctx.send("Error fetching song from YouTube.")
            return None

        if not self._is_playing:
            self._play_next_song(ctx)

    @commands.command(name="leave", aliases=["disconnect", 'l', 'L'])
    async def leave(self, ctx):
        """
        Command to instruct the bot to disconnect from the voice channel. If 
        not in a voice channel this command does nothing.
        
        Args:
            ctx (discord.ext.commands.Context): Discord Context object 
                containing information about the command request.
        """
        if ctx.voice_client:
            self._title_list.clear()
            self._song_queue.clear()
            await ctx.send(f"Disconnected {ctx.voice_client.channel.name}.")
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("Not in a voice channel...")

    @commands.command(name="pause")
    async def pause(self, ctx):
        """
        Command to pause the current song that is being played. If the current 
        track is already paused then it will unpause the track.

        Args:
            ctx (discord.ext.commands.Context): Discord Context object 
                containing information about the command request.
        
        Raises:
            SongException (Exception): if the track is not playing or paused.
        """

        if self._voice._is_playing():
            self._voice.pause()
            await ctx.send("Successfully paused.")
        elif self._voice.is_paused():
            self._voice.resume()
            await ctx.send("Successfully resumed.")
        else:
            await ctx.send("Unable to pause/resume")
            raise SongException("Unable to pause/resume.")

    @commands.command(name="skip", aliases=['s', 'S'])
    async def skip(self, ctx):
        """
        Command to skip the currently playing song and proceed to the next song 
            in the queue.
        
        Args:
            ctx (discord.ext.commands.Context): Discord Context object 
                containing information about the command request.
        """

        if self._voice._is_playing() or self._voice.is_paused():
            self._voice.stop()
            await ctx.send(f"Skipped song {self._current_song}")

    @commands.command(name="queue", aliases=['q', 'Q'])
    async def queue(self, ctx):
        """
        Command to show the current songs in the queue. Displays the queue as a
            discord message.

        Args:
            ctx (discord.ext.commands.Context): Discord Context object 
                containing information about the command request.
        """

        if len(self._title_list) < 1:
            await ctx.send("No songs in queue.")
            return

        queue = "Queue: "

        for song_index, song_title in enumerate(self._title_list, start=1):
            queue = queue + "\n" + str(song_index) + '. ' + song_title

        await ctx.send("**" + queue + "**")

    @commands.command(name="remove", aliases=['r', 'R'])
    async def remove(self, ctx):
        """
        Command to remove the specified song from the queue. The message should
            be formatted containing the index of the song in the queue starting 
            at 1.

        Args:
            ctx (discord.ext.commands.Context): Discord Context object 
                containing information about the command request.
        """
        index = ctx.message.content
        song_index = int(index.split(None, 1)[1]) - 1
        if -1 < song_index < len(self._song_queue):
            self._song_queue.pop(song_index)
            title = self._title_list.pop(song_index)
            await ctx.send("Removed: **" + str(song_index + 1) + '. ' + title + '**')
        else:
            await ctx.send("Invalid input brainless idjit")
    
    def _play_next_song(self, ctx):
        """
        Private helper function to play the next song in queue if it exists

        Args:
            ctx (discord.ext.commands.Context): Discord Context object 
                containing information about the command request.
        """
        if len(self._song_queue) > 0:
            self._is_playing = True

            song_url = self._song_queue.pop(0)
            song_title = self._title_list.pop(0)

            channel_id = ctx.channel.id
            channel = self._bot.get_channel(channel_id)

            # After the song has finished playing, send self._play_next_song
            self._voice.play(discord.FFmpegOpusAudio(song_url,
                                                    **FFMPEG_OPTIONS),
                            after=lambda x: self._play_next_song(ctx))
            self._bot.loop.create_task(
                channel.send(f"Playing song {song_title}"))
        else:
            self._is_playing = False

    async def _queue_song(self, song_name: str) -> str:
        """
        Private helper function to queue up the song from YouTube.

        Args:
            song_name (str): The name of the requested song as a string.
        
        Returns:
            (str): The title of the song as a string.
        
        Raises:
            SongException (Exception): If the song was unable to be fetched 
                from YouTube.
        """
        song_information = await fetch_song(song_name)
        if song_information:
            self._title_list.append(song_information['entries'][0]['title'])
            self._song_queue.append(song_information['entries'][0]['url'])
            return song_information['entries'][0]['title']
        else:
            raise SongException("Unable to fetch song from YouTube.")

    async def _join_voice(self, ctx):
        """
        Helper function to join the voice channel of the user that requested 
        the command.

        Args:
            ctx (discord.ext.commands.Context): Discord Context object 
                containing information about the command request.
        """
        if self._voice is None:
            if ctx.author.voice:
                channel = ctx.message.author.voice.channel
                self._voice = await channel.connect()
            else:
                await ctx.send(
                    "Must be in a voice channel to use this command.")
                raise JoinException("Not in voice channel")
        else:
            try:
                channel = ctx.message.author.voice.channel
                self._voice = ctx.voice_client
                await ctx.voice_client.move_to(channel)
            except:
                if ctx.author.voice:
                    channel = ctx.message.author.voice.channel
                    self._voice = await channel.connect()


async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))
