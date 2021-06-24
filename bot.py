import discord
import random
import datetime
import pytz
import wikipedia
import os
from decouple import config

from mcstatus import MinecraftServer
from discord.ext import commands

prefix = config('DISCORD_BOT_PREFIX')
# prefix = config('DISCORD_BOT_TEST_PREFIX')    #! Test
client = commands.Bot(command_prefix=prefix)
tz = pytz.timezone("Asia/Calcutta")

@client.event
async def on_ready():
    print("NNJGBot: Connection successful Status: READY")

TOKEN = config('DISCORD_BOT_TOKEN')
# TOKEN = config('DISCORD_BOT_TEST_TOKEN') #! Debug Bot Token

print(TOKEN)

def get_server_ping():
    server = MinecraftServer.lookup(os.environ.get("MCSERVER_IP"))
    # server = MinecraftServer.lookup(os.environ.get("DEBUG_MCSERVER_IP")) #! Debug MC server IP

    try:
        status = server.status()
    except:
        return None

    return status.players.online, status.latency

@client.command(aliases=["status", "serverstatus", "serverinfo"])
async def ping(ctx):
    server_ip = os.environ.get("MCSERVER_IP")
    res_list = ["hi", "pong", "AY", "ok", "Ok", "Yessir", "You called?", "Mhm?", "Whag", "What", "oki", "oke"]

    embed = discord.Embed(
        title="NNJG Minecraft Server Ping",
        description=f"{random.choice(res_list)}",
        color=discord.Color.gold(),
        timestamp=datetime.datetime.utcnow()
    )
    
    if get_server_ping() is not None:
        num_online, latency = get_server_ping()

        embed.add_field(name="Status", value="**ONLINE**", inline=True)
        embed.add_field(name="IP", value=f"`{server_ip.split(':')[0]}`", inline=True)
        embed.add_field(name="Port", value=f"`{server_ip.split(':')[1]}`", inline=True)
        embed.add_field(name="Players Online", value=f"`{num_online}`", inline=True)
        embed.add_field(name="Latency (ping)", value=f"`{latency}`", inline=True)
        message = "**Server is Online** :)"
    
    else:
        embed.add_field(name="Status", value="**OFFLINE**", inline=True)
        message = "**The NNJG Server is currently Offline. Please Ping @Minecraft Server Admin if you want it started** :)"

    embed.set_footer(text="SpudBot says hi :)")
    embed.set_author(name="SpudBot")

    await ctx.send(embed=embed)
    await ctx.send(message)


@client.command(aliases=["8ball", "eight-ball", "prophecy", "spudball"])
async def eightball(ctx, *, question=None):
    if question is None or all(list(question)) == " ":
        embed = discord.Embed(
            title=":8ball: THE SPUDBALL SAYS: :8ball:",
            description="_You didnt ask me a question lmao_",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Command Syntax: ", value="`$8ball (your question goes here, without the brackts lol)`", inline=True)

    else:
        res_list = [
            "Yee", "Definitely", "Whag no", "Lmao no way", "Mayhaps", "Maybe idk",
            "Why you askin' me\n I'm just a poor ~~boy~~ bot from a poor family\nSpare me my life from this monstrosity\nGALILEO GALILEO GALILEO FIGAR- ok ill stop",
            "Seems likely", "Ye", "No idiot", "Yes idiot", "Why would you even ask that question?", "Yesn't", "Ok", "If you say so",
            "69420", "Elephant", "My sources ~~google~~ say yes", "My sources ~~google~~ say no",
            "Poor connection try again", "Mayhaps", "Uhhhhhh lemme see... lmao jk screw you", "cate", "doge",
            "SPUDBOT_CRITICAL_ERROR: 001 STUPID_QUESTION", "Beep boop. Boop beep?", "Yes", "No", "Aye matey", "Nay matey",
            "As ze French like to say it, \"Oui\".", "As ze French like to say it, \"Non\".", "Doubtful", "Truly good sir",
            "No I don't think I will.", "Get outta my room im playing minecraft", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "No",
            "No", "No", "No", ":look of superiority: P e r h a p s" 
        ]
        embed = discord.Embed(
            title=":8ball: THE SPUDBALL SAYS: :8ball:",
            description=f"_{random.choice(res_list)}_",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )
    
    embed.set_footer(text="SpudBot says hi :)")
    embed.set_author(name="The Spudball")
    await ctx.send(embed=embed)

"""
* AI/Chatbot
"""

def get_wiki_response(query):
    try:
        return wikipedia.summary(query, auto_suggest=False)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query, auto_suggest=False)
            except Exception:
                pass
    return "_I couldn't find anything about your question on Wikipedia :/_"

@client.command(aliases=["wikipedia"])
async def wiki(ctx, *, query):
    response = get_wiki_response(query)

    if len(response) <= 2048:
        embed = discord.Embed(
            title=query,
            description=response,
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        
        embed.set_author(name="SpudBot the All-Knowing")
        embed.set_footer(text="Page 1/1 • SpudBot can search Wikipedia lol")

        await ctx.send(embed=embed)
    
    else:
        embed_list = []
        n = 2048
        embed_list = [response[i:i+n] for i in range(0, len(response), n)]
        for num, item in enumerate(embed_list, start=1):
            if (num == 1):
                embed = discord.Embed(
                    title=query,
                    description=item,
                    color=discord.Color.blurple()
                )
                embed.set_footer(text=f"Page {num} • SpudBot can search Wikipedia lol")
                embed.set_author(name="SpudBot the All-Knowing")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=item,
                    color=discord.Color.blurple()
                )
                embed.set_footer(text=f"Page {num} • SpudBot can search Wikipedia lol")
                await ctx.send(embed=embed)

"""
* Moderation
"""

@client.command(aliases=["clr", "cc", "delete"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amt=1):
    await ctx.channel.purge(limit=amt+1)

client.run(TOKEN)
