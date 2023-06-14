# =============================================================================
#
# Title: main.py
#
# Author: Aidan
#
# Description: Script to interface with bot commands, uses the discord.py package.
#              API reference for the discord.py can be found at
#              https://discordpy.readthedocs.io/en/stable/ext/commands/api.html
#
# =============================================================================

# =============================================================================
#
#                                     Imports
#
# =============================================================================
import os
import asyncio
import re
import nest_asyncio
import discord
import my_flask
from discord.ext import commands
from clip_commands.clip_downloader.clip_downloader import download_video, extract_video_link

# =============================================================================
#
#                               Constant Declaration
#
# =============================================================================
nest_asyncio.apply()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)
outplayed_pattern = r"https://outplayed\.tv/media/.*"


# bot.add_cog(RiotCommands(bot))

# =============================================================================
#
#                                   Events
#
# =============================================================================


@bot.event
async def on_ready():
    """
    Defines behavior when the bot is initialized.
    """
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    """
    Defines behavior when a message is sent to a discord channel
    :param message: The contents of the message sent, as a String.
    """
    await bot.process_commands(message)
    if message.author == bot.user:
        return None

    content = message.content.lower()

    if re.search(outplayed_pattern, content):
        # Get the outplayed link from the message
        try:
            outplayed_link = re.search(outplayed_pattern, content).group()
        except:
            print("Error has occurred in finding link")

        # Get vido title from rest of message
        video_title = re.sub(outplayed_pattern, "", content)

        # Get the video link and download the video
        video_link = extract_video_link(outplayed_link)
        download_video(video_link)


# =============================================================================
#
#                                   Logistics
#
# =============================================================================

async def load():
    """
    Loads the cogs before starting the bot
    Source: https://www.youtube.com/watch?v=hxsGrMijgUA
    """
    await bot.load_extension("music_commands.music_commands")
    await bot.load_extension("riot.riot_requests")


async def main():
    async with bot:
        await load()
        try:
            await bot.run(os.environ['Discord_test_token'])
        except:
            os.system("kill 1")


# Allows the bot to be pinged by uptime robot
# Source: https://www.youtube.com/watch?v=-5ptk-Klfcw
my_flask.keep_alive()
if __name__ == '__main__':
    asyncio.run(main())
