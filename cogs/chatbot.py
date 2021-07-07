import discord
import wikipedia
import datetime
from discord.ext import commands
from decouple import config
from prsaw import RandomStuff


class WikipediaCommands:
    def __init__(self):
        pass
    
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
    
    def get_wiki(self, query):
        response = self.get_wiki_response(query)
        if len(response) <= 2048:
            response_list = []
            embed = discord.Embed(
                title=query,
                description=response,
                color=discord.Color.blurple(),
                timestamp=datetime.datetime.utcnow()
            )

            embed.set_author(name="SpudBot the All-Knowing")
            embed.set_footer(text="Page 1/1 • SpudBot can search Wikipedia lol")
            response_list.append(embed)
        
        else:
            response_list = []
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
                else:
                    embed = discord.Embed(
                        description=item,
                        color=discord.Color.blurple()
                    )
                    embed.set_footer(
                        text=f"Page {num} • SpudBot can search Wikipedia lol")
                
                response_list.append(embed)

        return response_list       


class ChatBotCommands:
    def __init__(self):
        self.API_KEY = config('CHATBOT_API_KEY')
        self.BotAPI = RandomStuff(self.API_KEY)

    
    def get_response(self, query=None):
        if query is None:
            embed = discord.Embed(
                description="Yeah?",
                color=discord.Color.blurple()
            )
        else:
            try:
                embed = discord.Embed(
                    description=self.BotAPI.get_ai_response(query)[0].get('message'),
                    color=discord.Color.blurple()
                )
            except:
                embed = discord.Embed(
                    description="Uh what?",
                    color=discord.Color.blurple()
                )
        
        return embed


class Chatbot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.wikipedia_commands = WikipediaCommands()
        self.chatbot_commands = ChatBotCommands()
        self.chatbot_channel_id = config('CHATBOT_CHANNEL_ID')
        # self.chatbot_channel_id = int(config('CHATBOT_TEST_CHANNEL_ID'))   #! Debug Chatbot Channel ID

    @commands.command(aliases=["wikipedia"])
    async def wiki(self, ctx, *, query):
        for embed in self.wikipedia_commands.get_wiki(query):
            await ctx.send(embed=embed)
    
    @commands.command(aliases=["chatbot", "ai"])
    async def chat(self, ctx, *, query):
        await ctx.send(embed=self.chatbot_commands.get_response(query))
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.channel.id == self.chatbot_channel_id:
            await message.reply(embed=self.chatbot_commands.get_response(message.content))


def setup(client):
    client.add_cog(Chatbot(client))
