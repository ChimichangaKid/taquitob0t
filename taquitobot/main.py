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
import asyncio
import re
import nest_asyncio
import discord
import random
import discord_tokens
from discord.ext import commands
from clip_commands.clip_downloader.clip_downloader_discord import (
    ClipDownloaderDiscord
)
from clip_commands.clip_editor.clip_prep import (
    ClipPrepValorant,
)
from clip_commands.clip_editor.clip_editor import (
    ClipEditor
)
from clip_commands.clip_uploader.clip_uploader import (
    YouTubeUploader
)

# =============================================================================
#
#                               Constant Declaration
#
# =============================================================================
nest_asyncio.apply()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)
outplayed_pattern = r"https://outplayed\.tv/.*"


trigger_words = [
    "idjit", "val", "taquito", "taquitobot", "mald", "gg ", "GG ", "gnome",
    "michael", "bot", "tft", "boy savior", "savior", "meds", "braindead"
]
responses = [
    "Dog", "Mald", "little aram", "Bruh", "so bad", "where the idjits at",
    "my name mickle L", "lil tft", "Im the better zenyatta", ":skull:",
    "Ur a clown", "so braindead", "mald manlet", "i am laplaces demon",
    "troll", "I hate meatriders", "<:mpog:935384866369974332>", "noob",
    "keep taking notes buddy :nerd:", "Ur a mutt", "lil pool"
]

ochre99 = 331906932388659201
innoturtle = 314169544975319041
gogochonga = 329473509237587968
sarin = 144648633285869568
fishz = 293528843291983872
el_curry = 319282361978322957
drewpy = 369279788046614531

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
    
    if re.search(outplayed_pattern, content, re.IGNORECASE):
        clip_downloader = ClipDownloaderDiscord(discord_message=content)
        file_name = clip_downloader.download_video()
        game_title = clip_downloader.get_game_title()
        video_title = clip_downloader.get_video_title()
        match game_title:
            case "Valorant":
                clip_prep = ClipPrepValorant(video_file=file_name)
            case _:
                clip_prep = ClipPrepValorant(video_file=file_name)

        clip_editor = ClipEditor(clip_prep=clip_prep)  
        edited_clip = clip_editor.edit_and_save_video(clip_file=file_name, 
                                                      game_title=game_title,
                                                      video_title=video_title)
        
        clip_uploader = YouTubeUploader(video_title=video_title,
                                        game_title=game_title)
        try:
            video_link = clip_uploader.upload_to_youtube(file_name=edited_clip)
            await message.channel.send(video_link)
        except Exception as e:
            print("error uploading video")
            print(e)
        finally:
            clip_editor.remove_footage(edited_clip)
            clip_editor.remove_footage(file_name)      

    else:
        content = "".join(content.split()).lower()
        
    if any(word in content for word in trigger_words):
        random.seed()
        randNum = random.randint(0, 10)

        await message.channel.send(random.choice(responses))
        if randNum == 5:
            await message.channel.send("RAAAAAAAAAAAAAHHHH")
        if message.author.id == drewpy and randNum == 4:
            await message.channel.send("oh yeah lil bro?")
        if randNum == 3:
            await message.channel.send("I hate " +
                                       message.content.split(" ")[0])
        if randNum == 6:
            await message.channel.send("You're so mad")
            await message.channel.send("Stay mad")

    if "drew" in content:
        await message.channel.send("drew :peacock:")

    if "deez" in content:
        await message.channel.send(":face_with_raised_eyebrow:")

    if "leaf" in content:
        await message.channel.send(
            "https://tenor.com/view/toronto-maple-leafs-leafs-fans-first-round-exit-gif-25190957"
        )

    if "roster" in content:
        if message.author.id == innoturtle or message.author.id == fishz:
            await message.channel.send("Dogshit roster")
        if message.author.id == gogochonga:
            await message.channel.send("not fatribbit")
        if message.author.id == ochre99:
            await message.channel.send("God tier roster")
        if message.author.id == sarin:
            await message.channel.send("David please carry")
        if message.author.id == drewpy:
            await message.channel.send("ur literally silver")
        if message.author.id == el_curry:
            await message.channel.send("ur literally so bad")
            await message.channel.send("I mean, *nice try*")

    if "rope" in content:
        await message.channel.send("https://outplayed.tv/media/VnGLyd")
    
    if re.search(r'lil(?:ttle)?bro(?:ther)?|lilbr0', content):
        await message.channel.send("https://outplayed.tv/media/VnGLyd")
    
    if "littleb" in content:
        await message.channel.send("https://outplayed.tv/media/VnGLyd")
        

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
    await load()
    await bot.run(discord_tokens.TAQUITOBOT_TOKEN)

            


# # Allows the bot to be pinged by uptime robot
# # Source: https://www.youtube.com/watch?v=-5ptk-Klfcw
# my_flask.keep_alive()
if __name__ == '__main__':
    asyncio.run(main())
