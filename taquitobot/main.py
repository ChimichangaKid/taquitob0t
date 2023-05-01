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
import nest_asyncio
import discord
import my_flask
from discord.ext import commands

# =============================================================================
#
#                               Constant Declaration
#
# =============================================================================
nest_asyncio.apply()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

#bot.add_cog(RiotCommands(bot))

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

    content = message.content


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
