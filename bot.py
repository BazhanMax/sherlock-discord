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


client.run(token)
