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
import json
import requests
from discord.ext import commands
from bs4 import BeautifulSoup

# =============================================================================
#
#                                     Constants
#
# =============================================================================

NOT_EARNED_FLAG = "chest notEarned"


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

    @commands.Cog.listener()
    async def on_ready(self):
        print("riot_commands ready")

    # =============================================================================
    #
    #                                   Commands
    #
    # =============================================================================

    @commands.command(name="chest", aliases=['c', 'C'])
    async def check_chest_available(self, ctx, username: str, champion: str, region: str = 'na'):
        """
        Command to request if a champion mastery chest is available in League of Legends by Riot Games.

        :param ctx: A discord.Context object, represents the context of the command being issued.
        :param username: A string representation of the username of the player. Should be a valid league of legends
        username.
        :param champion: A string representation of the champion name in question
        :param region: A string representation of the region name of the player in question. Defaults to na
        (North America). See https://leagueoflegends.fandom.com/wiki/Servers for details on valid prefixes.
        """
        # Properly format variables
        champion_name = champion.title()
        champion_mastery_webpage = 'https://championmastery.gg/summoner?summoner=' + username + '&region=' + region

        # Get webpage data via requests package and Beautiful Soup
        webpage_data = requests.get(champion_mastery_webpage)
        parsed_webpage_data = BeautifulSoup(webpage_data.text, 'html.parser')

        # Every champion on the webpage is divided into <tr> </tr> blocks, so simply splitting the
        # data via these flags is possible
        champion_specific_data = parsed_webpage_data.find_all('tr')

        # Iterate over all champion data until the champion is found
        for champion_data in champion_specific_data:
            champion_data_text = champion_data.prettify()
            if champion_name in champion_data_text:
                if NOT_EARNED_FLAG in champion_data_text:
                    await ctx.send("Chest available <:mpog:935384866369974332>")
                    return None
                else:
                    await ctx.send("Chest unavailable")
                    return None

        # If the champion name is invalid
        await ctx.send("Champion not found")

    @commands.command(name="register-user", aliases=['ru', 'Ru', 'add-user', 'au', 'Au'])
    async def register_user(self, ctx, *, username):
        # TODO: Implement code that uses this command
        """
        Command to register the user in the database to make the chest command faster, links the discord id with riot
        account in the bot via json file.
        :param ctx: A discord.Context object, represents the context of the command being issued.
        :param username: The username to be linked to this discord id, should be a string.
        """
        username = username.lower()
        users = json.loads(open("taquitobot/riot/usernames.json").read())
        for user_list in users["users"]:
            # Check if the discordID already exists
            if ctx.message.author.id == user_list['discord']:
                old_riot_ids = user_list['riot']
                if username in old_riot_ids:
                    await ctx.send("Username already linked.")
                    return None
                else:
                    await ctx.send(f"Added {username} to {ctx.message.author}'s linked IDs")
                    old_riot_ids.append(username)

                    # Write the new username to the file
                    with open("taquitobot/riot/usernames.json", "w") as outfile:
                        json.dump(users, outfile, indent=4)

                    return None
        await ctx.send(f"Adding new user {ctx.message.author}.")
        new_user = {
            "discord": ctx.message.author.id,
            "riot": [username]
        }
        users["users"].append(new_user)
        with open("taquitobot/riot/usernames.json", "w") as outfile:
            json.dump(users, outfile, indent=4)
        return None

    @commands.command(name="opgg", aliases=['op'])
    async def league_get_opgg(self, ctx, *, username):
        """
        Searches the op.gg profile of the specified user(s)

        :param ctx: A discord.Context object, represents the context of the command being issued.
        :param username: The name(s) of the players to be searched for as strings
        """
        name_list = username.split(" ")

        base_opgg_url = 'https://na.op.gg/'
        if len(name_list) == 1:
            url_addon = 'summoners/na/'
        else:
            url_addon = 'multisearch/na?summoners='

        for summoner_name in name_list:
            summoner_name_formatted = str(summoner_name).replace(" ", '%20')
            url_addon = url_addon + summoner_name_formatted + '%2C'

        full_url = base_opgg_url + url_addon
        await ctx.send(full_url[:-3])
        return None


async def setup(bot):
    await bot.add_cog(RiotCommands(bot))
