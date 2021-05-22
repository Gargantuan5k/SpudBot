import discord
import random
import time
import datetime
import pytz

from waiting import wait
from AternosAPI.aternosapi import AternosAPI as API
from discord.ext import commands

client = commands.Bot(command_prefix="$")
headers_cookie = open("bot-essentials/nnjg-properties/h-cookie.txt", "r").read()
nnjg_token = open("bot-essentials/nnjg-properties/token.txt", "r").read()

NNJG = API(headers=headers_cookie, TOKEN=nnjg_token)

tz = pytz.timezone("Asia/Calcutta")


def get_start_stop_embed(title, desc, icon_url=None, color=discord.Color.blue()):
    embed = discord.Embed(
        title=title, description=desc, colour=color, timestamp=datetime.datetime.utcnow()
    )
    embed.set_footer(text="SpudBot says hi :)")
    embed.set_author(name="SpudBot")
    if icon_url is not None:
        embed.set_image(url=icon_url)

    return embed


@client.event
async def on_ready():
    print("NNJGBot: Connection successful Status: READY")


tok_file = open("bot-essentials/token.txt", "r")
TOKEN = tok_file.read()


@client.command()
async def ping(ctx):
    res_list = ["hi", "pong", "AY", "ok", "Ok", "Yessir", "You called?", "Mhm?", "Whag", "What", "oki", "oke"]
    await ctx.send(f"{random.choice(res_list)}")
    time.sleep(0.5)
    await ctx.send(f"O did you mean my latency? {round(client.latency * 1000)}ms "
                   f"\nno way he")


@client.command(aliases=["8ball", "eight-ball", "prophecy", "answerme"])
async def eightball(ctx, *, question):
    res_list = [
        "Yee", "Definitely", "Whag no", "Lmao no way", "Mayhaps", "Maybe idk",
        "Why you askin' me I'm just a poor ~~boy from a poor family~~ discord bot", "Seems likely",
        "Ye", "No idiot", "Yes idiot", "Why would you even ask that question?", "Yesn't", "Ok", "If you say so",
        "69420", "Elephant", "My sources ~~google~~ say yes", "My sources ~~google~~ say no",
        "Poor connection try again",
        "SPUDBOT_CRITICAL_ERROR: STUPID_QUESTION_001", "Beep boop. Boop beep?", "Yes", "No", "Aye matey", "Nay matey",
        "As ze French like to say it, \"Oui\".", "As ze French like to say it, \"Non\".", "Doubtful", "Truly good sir",
        "No I don't think I will."
    ]
    await ctx.send(f"{random.choice(res_list)}")


@client.command(aliases=["serverstart", "start-server", "ss", "start"])
async def start_server(ctx):
    if NNJG.GetStatus() == "Online":
        embed = get_start_stop_embed("NNJG Official Minecraft Server",
                                                  f":ballot_box_with_check: Server is now Online {ctx.author.mention}!"
                                                  "\nJoin the game!\n",
                                                  color=discord.Color.gold())

        embed.add_field(name="IP", value="`nnjg.ml`", inline=True)
        embed.add_field(name="Port", value="34387", inline=True)
        embed.add_field(name="Status", value=NNJG.GetStatus(), inline=True)

    elif NNJG.GetStatus() == "Offline":
        NNJG.StartServer()
        await ctx.send(f"{ctx.author.mention} Server is starting, please wait for my confirmation ...")

        def server_on():
            return NNJG.GetStatus() == "Online"

        wait(lambda: server_on())

        embed = get_start_stop_embed("NNJG Official Minecraft Server",
                                                  f":ballot_box_with_check: Server is now Online {ctx.author.mention}!"
                                                  "\nYou can join the server now :).\n",
                                                  color=discord.Color.green())
        embed.add_field(name="IP", value="`nnjg.ml`", inline=True)
        embed.add_field(name="Port", value="34387", inline=True)
        embed.add_field(name="Status", value=NNJG.GetStatus(), inline=True)

        await ctx.send(embed=embed)


@client.command(aliases=["serverstop", "stop-server", "sts", "stop"])
async def stop_server(ctx):
    if NNJG.GetStatus() == "Online":
        NNJG.StopServer()
        await ctx.send(f"{ctx.author.mention} Server is stopping, please wait for my confirmation ...")

        def server_on():
            return NNJG.GetStatus() == "Online"

        wait(lambda: not server_on())

        await ctx.send(embed=get_start_stop_embed(f"NNJG Official Minecraft Server",
                                                  f":ballot_box_with_check:  {ctx.author.mention} Server is now Offline!"
                                                  "\nUse `$start-server` to start it again.",
                                                  color=discord.Color.red()))

    elif NNJG.GetStatus() == "Offline":
        await ctx.send(embed=get_start_stop_embed("NNJG Official Minecraft Server", f":x: {ctx.author.mention} Server is already Offline!\n"
                                                                                    "\nSay `$start-server` to start "
                                                                                    "it again!",
                                                  color=discord.Color.gold()))


@client.command(aliases=["srestart", "server-restart", "restart-server"])
async def restart_server(ctx):
    if NNJG.GetStatus() == "Offline":
        await ctx.send(ctx.author.mention + " The server is currently Offline so I'll just start it")
        await start_server(ctx)
    elif NNJG.GetStatus() == "Online":
        await ctx.send(ctx.author.mention + " Restarting server, please wait for my confirmation")

        def server_on():
            return NNJG.GetStatus() == "Online"

        wait(lambda: server_on())

        embed = get_start_stop_embed("NNJG Official Minecraft Server (RESTARTED)",
                                                  f":ballot_box_with_check: Server is now Online {ctx.author.mention}!"
                                                  "\nYou can join the server now :).\n",
                                                  color=discord.Color.green())
        embed.add_field(name="IP", value="`nnjg.ml`", inline=True)
        embed.add_field(name="Port", value="34387", inline=True)
        embed.add_field(name="Status", value=NNJG.GetStatus(), inline=True)

        await ctx.send(embed=embed)


@client.command(aliases=["server-status", "sstatus", "serverstatus", "serverinfo", "server-info", "server_info", "sinfo"])
async def server_status(ctx):
    status = NNJG.GetStatus()
    embed = discord.Embed(
        title="NNJG Official Minecraft Server Status",
        description=f"{ctx.author.mention} Server is currently {status}. To start/stop the server, please use the appropriate commands :).",
        timestamp=datetime.datetime.utcnow(), color=discord.Color.blue()
    )
    embed.add_field(name="IP", value="`nnjg.ml`", inline=True)
    embed.add_field(name="Port", value="34387", inline=True)
    embed.add_field(name="Status", value=status, inline=True)

    embed.set_footer(text="SpudBot says hi :).")

    await ctx.send(embed=embed)


client.run(TOKEN)
