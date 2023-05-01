# =============================================================================
#
# Title: riot_requests.py
#
# Author: Aidan
#
# Description: Script to interface with Riot Games related commands.
#
# =============================================================================

# =============================================================================
#
#                                     Imports
#
# =============================================================================

import discord
from discord.ext import commands

# =============================================================================
#
#                                     Classes
#
# =============================================================================


class RiotCommands(commands.Cog):
    """
    Representation Invariant:
    Abstraction Function:
        A RiotCommands object represents a gateway to access Riot Games related data from the discord bot.
    """

    def __init__(self, bot):
        self.bot = bot

    # =============================================================================
    #
    #                                   Commands
    #
    # =============================================================================

    @commands.command(name="chest", aliases=['c', 'C'])
    async def check_chest_available(self, ctx, *args):
        """
        Command to request if a champion mastery chest is available in League of Legends by Riot Games.
        :param ctx: A discord.Context object, represents the context of the command being issued.
        :param args:
        :return:
        """
        return None