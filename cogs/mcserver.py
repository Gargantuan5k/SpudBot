import discord
import random
import datetime
from discord.ext import commands
from decouple import config
from mcstatus import MinecraftServer


class MCServer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.MCSERVER_IP = config('MCSERVER_IP')
        self.DEBUG_MCSERVER_IP = config('DEBUG_MCSERVER_IP')

    
    def get_server_ping(self):
        server = MinecraftServer.lookup(self.MCSERVER_IP)
        # server = MinecraftServer.lookup(self.DEBUG_MCSERVER_IP) #! Debug MC server IP

        try:
            status = server.status()
        except:
            return None

        return status.players.online, status.latency


    @commands.command(aliases=["status", "serverstatus", "serverinfo"])
    async def ping(self, ctx):
        server_ip = self.MCSERVER_IP
        # server_ip = self.DEBUG_MCSERVER_IP  #! Debug ip
        res_list = ["hi", "pong", "AY", "ok", "Ok", "Yessir", "You called?", "Mhm?", "Whag", "What", "oki", "oke"]

        embed = discord.Embed(
            title="NNJG Minecraft Server Ping",
            description=f"{random.choice(res_list)}",
            color=discord.Color.gold(),
            timestamp=datetime.datetime.utcnow()
        )

        if self.get_server_ping() is not None:
            num_online, latency = self.get_server_ping()

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


def setup(client):
    client.add_cog(MCServer(client))
