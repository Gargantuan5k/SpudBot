import discord
import datetime
import random
import asyncio
import praw

from discord.ext import commands
from decouple import config


class RedditCommand:
    def __init__(self):
        self.REDDIT_CLIENT_ID = config('REDDIT_CLIENT_ID')
        self.REDDIT_CLIENT_SECRET = config('REDDIT_CLIENT_SECRET')
        self.REDDIT_USERNAME = config('REDDIT_USERNAME')
        self.REDDIT_USER_AGENT = config('REDDIT_USER_AGENT')
        self.REDDIT_PASSWORD = config('REDDIT_PASSWORD')


        self.Reddit = praw.Reddit(
            client_id=self.REDDIT_CLIENT_ID,
            client_secret=self.REDDIT_CLIENT_SECRET, 
            username=self.REDDIT_USERNAME, 
            password=self.REDDIT_PASSWORD, 
            user_agent=self.REDDIT_USER_AGENT
        )
    
    def random_reddit_submission(self, sub_name):
        sub= self.Reddit.subreddit(sub_name)
        all_submissions = []
        top = sub.top(limit=50)

        for submission in top:
            all_submissions.append(submission)
        
        ret_submission = random.choice(all_submissions)
        submission_name = ret_submission.title
        url = ret_submission.url

        embed = discord.Embed(
            url="https://reddit.com" + ret_submission.permalink,
            title=f"{submission_name}" if ret_submission.title is not None else f"[Untitled Post]",
            color = discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
        )

        try:
            embed.set_image(url=url)
        except:
            pass
        embed.set_author(name=f"Posted by u/{ret_submission.author.name}" if ret_submission.author.name is not None else f"u/[DELETED]")
        embed.set_footer(text=f"👍 {int(ret_submission.score)} 💬 {int(ret_submission.num_comments)}  •  In r/{sub}")

        return embed
    

class OtherCommand:
    def __init__(self):
        pass

    def eight_ball(self, question):
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
                "SPUDBOT-CRITICAL-ERROR: 001 STUPID-QUESTION",
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
                "Yee",
                "Yee",
                "Yes",
                "No",
                "No",
                "No",
                "No",
                "No",
                ":look of superiority: P e r h a p s",
                "Idk about that but time for some shameless self-promotion: Use the `$reddit` command to view a random post from a subreddit lol"]
            embed = discord.Embed(
                title=":8ball: THE SPUDBALL SAYS: :8ball:",
                description=f"_{random.choice(res_list)}_",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )

        embed.set_footer(text="SpudBot says hi :)")  
    
        return embed



class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit_command = RedditCommand()
        self.other_command = OtherCommand()

    @commands.command(aliases=["8ball", "eight-ball", "prophecy", "spudball"])
    async def eightball(self, ctx, *, question=None):
        await ctx.send(embed=self.other_command.eight_ball(question))

    
    @commands.command(aliases=["meem", "maymay", "fune"])
    async def meme(self, ctx):
        await ctx.send(embed=self.reddit_command.random_reddit_submission(sub_name="memes"))
    

    @commands.command(aliases=["randomreddit", "reddit"])
    async def redditrandom(self, ctx, *, sub=None):
        if sub is not None:
            try:
                if sub.startswith("r/"):
                    sub = sub[2:]
                await ctx.send(embed=self.reddit_command.random_reddit_submission(sub_name=sub))
            except:
                await ctx.send("That subreddit either doesn't exist or is private oof")
        else:
            await ctx.send(f"Bruv specify a subreddit please ```{config('DISCORD_BOT_PREFIX')}redditrandom r/subreddit```")


def setup(client):
    client.add_cog(Fun(client))
