# DS Bot for [Sherlock project](https://github.com/sherlock-project/sherlock)

This is a Discord bot for the Sherlock project that searches for a given username on various websites. The bot uses Discord's slash commands feature to take input from the user and return the search results.

## Setup

To use the bot, follow the instructions below:

1. install the sherlock: `pip install sherlock-project`
2. Fill in the necessary values in `botconfig.ini` file. your bot must have `applications.commands`, `bot` scopes and `send messages` permission. `guild-id` - server id.
3. Install the dependencies: `pip install discord.py`.
4. Run the bot using `python bot.py`.

## Usage

To search for a username using the bot, use the following slash command in discord:

```
/search <username> <timeout> <nsfw>
```

- `username`: The username to search for.
- `timeout`: The timeout in seconds for the search minimum is 1.
- `nsfw`: Whether to include NSFW websites in the search or not.

The bot will then return the search results in separate messages on Discord. If the search results are too long, the bot will split the messages into multiple parts.
