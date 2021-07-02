import discord
import wikipedia
import datetime
from discord.ext import commands


class Chatbot(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_wiki_response(self, query):
        try:
            return wikipedia.summary(query, auto_suggest=False)
        except Exception:
            for new_query in wikipedia.search(query):
                try:
                    return wikipedia.summary(new_query, auto_suggest=False)
                except Exception:
                    pass
        return "_I couldn't find anything about your question on Wikipedia :/_"


    @commands.command(aliases=["wikipedia"])
    async def wiki(self, ctx, *, query):
        response = self.get_wiki_response(query)

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
            embed_list = [response[i:i + n] for i in range(0, len(response), n)]
            for num, item in enumerate(embed_list, start=1):
                if num == 1:
                    embed = discord.Embed(
                        title=query,
                        description=item,
                        color=discord.Color.blurple()
                    )
                    embed.set_footer(
                        text=f"Page {num} • SpudBot can search Wikipedia lol")
                    embed.set_author(name="SpudBot the All-Knowing")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        description=item,
                        color=discord.Color.blurple()
                    )
                    embed.set_footer(
                        text=f"Page {num} • SpudBot can search Wikipedia lol")
                    await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Chatbot(client))
