import discord
import datetime
import random

from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["8ball", "eight-ball", "prophecy", "spudball"])
    async def eightball(self, ctx, *, question=None):
        if question is None or all(list(question)) == " ":
            embed = discord.Embed(
                title=":8ball: THE SPUDBALL SAYS: :8ball:",
                description="_You didnt ask me a question lmao_",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(
                name="Command Syntax: ",
                value="`$8ball (your question goes here, without the brackts lol)`",
                inline=True)

        else:
            res_list = [
                "Yee",
                "Definitely",
                "Whag no",
                "Lmao no way",
                "Mayhaps",
                "Maybe idk",
                "Why you askin' me\n I'm just a poor ~~boy~~ bot from a poor family\nSpare me my life from this monstrosity\nGALILEO GALILEO GALILEO FIGAR- ok ill stop",
                "Seems likely",
                "Ye",
                "No idiot",
                "Yes idiot",
                "Why would you even ask that question?",
                "Yesn't",
                "Ok",
                "If you say so",
                "69420",
                "Elephant",
                "My sources ~~google~~ say yes",
                "My sources ~~google~~ say no",
                "Poor connection try again",
                "Mayhaps",
                "Uhhhhhh lemme see... lmao jk screw you",
                "cate",
                "doge",
                "SPUDBOT_CRITICAL_ERROR: 001 STUPID_QUESTION",
                "Beep boop. Boop beep?",
                "Yes",
                "No",
                "Aye matey",
                "Nay matey",
                "As ze French like to say it, \"Oui\".",
                "As ze French like to say it, \"Non\".",
                "Doubtful",
                "Truly good sir",
                "No I don't think I will.",
                "Get outta my room im playing minecraft",
                "Yes",
                "Yes",
                "Yes",
                "Yes",
                "Yes",
                "No",
                "No",
                "No",
                "No",
                "No",
                ":look of superiority: P e r h a p s"]
            embed = discord.Embed(
                title=":8ball: THE SPUDBALL SAYS: :8ball:",
                description=f"_{random.choice(res_list)}_",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )

        embed.set_footer(text="SpudBot says hi :)")
        embed.set_author(name="The Spudball")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
