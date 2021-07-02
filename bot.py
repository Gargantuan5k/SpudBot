import random
import datetime
from decouple import config
from discord.ext import commands

prefix = config('DISCORD_BOT_PREFIX')
TOKEN = config('DISCORD_BOT_TOKEN')
# TOKEN = config('DISCORD_BOT_TEST_TOKEN') #! Debug Bot Token
# prefix = config('DISCORD_BOT_TEST_PREFIX')    #! Test
MCSERVER_IP = config("MCSERVER_IP")
DEBUG_MCSERVER_IP = config("DEBUG_MCSERVER_IP")

client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
    print("NNJGBot: Connection successful Status: READY")
    print(TOKEN)


cogs = ["commandevents", "fun", "administrator", "chatbot", "mcserver"]
if __name__ == "__main__":
    for cog in cogs:
        client.load_extension("cogs." + cog)

    client.run(TOKEN)
