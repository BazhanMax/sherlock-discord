import discord
from discord import app_commands 
from sherlock import *
import configparser
from threading import Thread
import threading
import asyncio
import queue

config = configparser.ConfigParser()
config.read('bot_config.ini')

guild_id = config.get('discord','guild_id')
token = config.get('discord','token')


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=guild_id)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"my nickname is [{self.user}]")

client = aclient()
tree = app_commands.CommandTree(client)


def sherFind(queue,nsfw,username,timeout,tor):
    query_notify = QueryNotifyPrint(result=None,
                                    verbose=False,
                                    print_all=False,
                                    browse=False)
    try:
        if False:
            sites = SitesInformation(os.path.join(
                os.path.dirname(__file__), "resources/data.json"))
        else:
            sites = SitesInformation(None)
    except Exception as error:
        print(f"ERROR:  {error}")
        sys.exit(1)

    if not nsfw:
        sites.remove_nsfw_sites()
    site_data_all = {site.name: site.information for site in sites}
    if None is None:
        # Not desired to look at a sub-set of sites
        site_data = site_data_all
    else:
        # User desires to selectively run queries on a sub-set of the site list.

        # Make sure that the sites are supported & build up pruned site database.
        site_data = {}
        site_missing = []
        for site in None:
            counter = 0
            for existing_site in site_data_all:
                if site.lower() == existing_site.lower():
                    site_data[existing_site] = site_data_all[existing_site]
                    counter += 1
            if counter == 0:
                # Build up list of sites not supported for future error message.
                site_missing.append(f"'{site}'")

        if site_missing:
            print(
                f"Error: Desired sites not found: {', '.join(site_missing)}.")

        if not site_data:
            sys.exit(1)


    results = sherlock(username,
                           site_data,
                           query_notify,
                           tor=tor,
                           unique_tor=None,
                           proxy=None,
                           timeout=timeout)

    results_list= []
    exists_counter = 0
    for website_name in results:
                dictionary = results[website_name]
                if dictionary.get("status").status == QueryStatus.CLAIMED:
                    exists_counter += 1
                    results_list.append(str(dictionary["url_user"]))


    queue.put(results_list)
    

def createSplitMsg(results_list):
    results_for_msg = ""
    msg_lists = []
    i = 0
    for link in results_list:
        i += 1
        prev = results_for_msg
        if len(results_for_msg)<1930:
            results_for_msg +=   "\n" + f"[{i}] > {link}"
        else:
            results_for_msg = ""
            msg_lists.append(prev)
    msg_lists.append(results_for_msg)
    return msg_lists






@tree.command(name = 'search',guild = discord.Object(id=guild_id), description='search username') #guild specific slash command
async def slashcmd(interaction, username: str,timeout: int, nsfw: bool):
    tor = False
    channel = interaction.channel
    await interaction.response.send_message(f"searching {username}")
    
    
    my_queue = queue.Queue()
    Thread_for_search = Thread(target=sherFind, args=(my_queue,nsfw,username,timeout,tor))
    Thread_for_search.start()
    
    while Thread_for_search.is_alive():
        await interaction.edit_original_response(content=f"searching {username} /")
        await asyncio.sleep(0.2)
        await interaction.edit_original_response(content=f"searching {username} -")
        await asyncio.sleep(0.2)
        await interaction.edit_original_response(content=f"searching {username} \\")
        await asyncio.sleep(0.2)
        await interaction.edit_original_response(content=f"searching {username} |")
        await asyncio.sleep(0.2)

    results_list = my_queue.get()
    Thread_for_search.join()
    
    msg_lists = createSplitMsg(results_list)
    await interaction.edit_original_response(content=f"[{username}]  found on [{len(results_list)}] sites:")
    for msg in msg_lists:
        await channel.send(str(msg))
    
 
client.run(token)