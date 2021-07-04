import discord
import datetime
import random
import praw

from discord.ext import commands
from decouple import config

REDDIT_CLIENT_ID = config('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = config('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = config('REDDIT_USERNAME')
REDDIT_USER_AGENT = config('REDDIT_USER_AGENT')
REDDIT_PASSWORD = config('REDDIT_PASSWORD')

Reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET, 
    username=REDDIT_USERNAME, 
    password=REDDIT_PASSWORD, 
    user_agent=REDDIT_USER_AGENT
)


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

    
    @commands.command(aliases=["meem", "maymay", "fune"])
    async def meme(self, ctx):
        sub = Reddit.subreddit("memes")
        all_submissions = []
        top = sub.top(limit=100)

        for submission in top:
            all_submissions.append(submission)
        
        ret_submission = random.choice(all_submissions)
        submission_name = ret_submission.title
        url = ret_submission.url

        embed = discord.Embed(
            url="https://reddit.com" + ret_submission.permalink,
            title=f"{submission_name}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_image(url=url)
        embed.set_footer(text=f"👍 {int(ret_submission.score)} 💬 {int(ret_submission.num_comments)}  •  In r/{sub}")
        embed.set_author(name=f"Posted by u/{ret_submission.author.name}")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
