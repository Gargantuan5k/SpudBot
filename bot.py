import discord
import random
import datetime
import pytz
import wikipedia

from mcstatus import MinecraftServer
from discord.ext import commands
from prsaw import RandomStuff
from math import e

rs = RandomStuff()
client = commands.Bot(command_prefix="$")
tz = pytz.timezone("Asia/Calcutta")

def get_chat_response(message): 
    return rs.get_ai_response(message)


@client.event
async def on_ready():
    print("NNJGBot: Connection successful Status: READY")


tok_file = open("bot-essentials/token.txt", "r")
TOKEN = tok_file.read()

#! DEBUG TOKEN (SpudBotTest) ln=28
# TOKEN = "ODU2NTIzMTk3NDQ4MzIzMDky.YNCRYw.31FVbwh-wUKdEuGOZy_25zrtiiw"

print(TOKEN)

def get_server_ping():
    server = MinecraftServer.lookup(open("bot-essentials/nnjg-properties/server-ip.txt", "r").read())

    #! DEBUG SERVER LOOKUP IP (ln=37)
    # server = MinecraftServer.lookup("namehaven.aternos.me:34387")

    try:
        status = server.status()
    except:
        return None

    return status.players.online, status.latency

@client.command(aliases=["status", "serverstatus", "serverinfo"])
async def ping(ctx):
    server_ip = open("bot-essentials/nnjg-properties/server-ip.txt", "r").read()
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


@client.command(aliases=["8ball", "eight-ball", "prophecy", "answerme"])
async def eightball(ctx, *, question):
    res_list = [
        "Yee", "Definitely", "Whag no", "Lmao no way", "Mayhaps", "Maybe idk",
        "Why you askin' me\n I'm just a poor ~~boy~~ bot from a poor family\nSpare me my life from this monstrosity\nGALILEO GALILEO GALILEO FIGAR- ok ill stop",
         "Seems likely", "Ye", "No idiot", "Yes idiot", "Why would you even ask that question?", "Yesn't", "Ok", "If you say so",
        "69420", "Elephant", "My sources ~~google~~ say yes", "My sources ~~google~~ say no",
        "Poor connection try again", "Mayhaps", "Uhhhhhh lemme see... lmao jk screw you", "cate", "doge",
        "SPUDBOT_CRITICAL_ERROR: 001 STUPID_QUESTION", "Beep boop. Boop beep?", "Yes", "No", "Aye matey", "Nay matey",
        "As ze French like to say it, \"Oui\".", "As ze French like to say it, \"Non\".", "Doubtful", "Truly g  ood sir",
        "No I don't think I will.", "Get outta my room im playing minecraft", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "No",
        "No", "No", "No" 
    ]
    await ctx.send(f"{random.choice(res_list)}")

client.run(TOKEN)
