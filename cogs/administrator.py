import discord
from discord.ext import commands

class Administrator(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["clr", "cc", "delete"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amt=1):
        await ctx.channel.purge(limit=amt + 1)


def setup(client):
    client.add_cog(Administrator(client))
