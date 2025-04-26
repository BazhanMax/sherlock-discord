import discord
from discord import app_commands
import sys
import os
import configparser
from threading import Thread
import threading
import asyncio
import queue

# sys.path.append("./sherlock-discord/sherlock-master/sherlock")
from sherlockClass import *


config = configparser.ConfigParser()
patchToFile = os.path.dirname(os.path.abspath(__file__))
config.read(f"{patchToFile}/botconfig.ini")

guild_id = config.get("discord", "guild_id")
token = config.get("discord", "token")


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = (
            False  # we use this so the bot doesn't sync commands more than once
        )

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # check if slash commands have been synced
            await tree.sync(
                guild=discord.Object(id=guild_id)
            )  # guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"my nickname is [{self.user}]")


client = aclient()
tree = app_commands.CommandTree(client)


# queue.put(results_list)
def Worker(obj, q):
    obj.Search()
    q.put(obj)


@tree.command(
    name="sherlock", guild=discord.Object(id=guild_id), description="search username"
)  # guild specific slash command
@app_commands.describe(username="Username to search",timeout="Website response timeout in seconds. 1 for quick search, 20 for advanced. It should be more then 0.",nsfw="This specify whether or not to include nsfw websites in search")
async def slashcmd(interaction, username: str, timeout: int, nsfw: bool):
    tor = False

    sherlock = Sherlock(username, timeout, tor, nsfw)

    channel = interaction.channel
    await interaction.response.send_message(f"searching {username}")

    q = queue.Queue()
    Thread_for_search = Thread(target=Worker, args=(sherlock, q))
    status = sherlock.getStatus()
    Thread_for_search.start()

    while Thread_for_search.is_alive():
        await interaction.edit_original_response(
            content=f"searching {username} [{status}] /"
        )
        await asyncio.sleep(0.2)
        await interaction.edit_original_response(
            content=f"searching {username} [{status}] -"
        )
        await asyncio.sleep(0.2)
        await interaction.edit_original_response(
            content=f"searching {username} [{status}] \\"
        )
        await asyncio.sleep(0.2)
        await interaction.edit_original_response(
            content=f"searching {username} [{status}] |"
        )
        await asyncio.sleep(0.2)

    sherlock = q.get()
    # results_list = my_queue.get()
    Thread_for_search.join()

    msg_lists = sherlock.getResultsMsgs()
    res_lists = sherlock.getResultsList()
    await interaction.edit_original_response(
        content=f"[{username}]  found on [{len(res_lists)}] sites:"
    )
    for msg in msg_lists:
        await channel.send(str(msg))

@tree.command(
    name="help", 
    guild=discord.Object(id=guild_id), 
    description="Show help message"
)
async def helpcmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Help for Sherlock discord bot",
        description="Thois is a bot for username search that provides ability to use Sherlock project in discord",
        color=0x00ff00
    )
    
    embed.add_field(
        name="Comands",
        value="`/sherlock [username] [timeout] [nsfw]` - start search",
        inline=False
    )
    
    embed.add_field(
        name="Documentation",
        value="""[Full Sherlock discord bot documentation on GitHub](https://github.com/BazhanMax/sherlock-discord)
        [Full Sherlock documentation on GitHub](https://github.com/sherlock-project/sherlock)""",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

client.run(token)
