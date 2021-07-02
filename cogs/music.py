import discord
import datetime
from discord.ext import commands
from youtube_dl import YoutubeDL


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.is_playing = False

        self.queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': 'vn'}

        self.vc = ''
    
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def play_next(self):
        if len(self.queue) > 0:
            self.is_playing = True
            url = self.queue[0][0]['source']

            self.queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS, executable="D:/Users/Siddharth/Program Files/ffmpeg/bin/ffmpeg.exe"), after=lambda e: self.play_next())
        else:
            self.is_playing = False
        
    async def play_music(self):
        if len(self.queue) > 0:
            self.is_playing = True

            url = self.queue[0][0]['source']

            if self.vc == '' or not self.vc.is_connected():
                self.vc = await self.queue[0][1].connect()
            else:
                self.vc = await self.client.move_to(self.queue[0][1])

            print(self.queue)
            self.queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS, executable="D:/Users/Siddharth/Program Files/ffmpeg/bin/ffmpeg.exe"), after=lambda e: self.play_next())
        else:
            self.is_playing = False
    
    @commands.command(aliases=['p', 'musicplay'])
    async def mplay(self, ctx, *args):
        query = " ".join(args)

        if ctx.author.voice is None:
            # voice_channel = ctx.author.voice.channel

            embed = discord.Embed(
                description=":x: Please connect to a voice channel first :)",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name="SpudBot")
            embed.set_footer(text="Why am I a DJ-")

            await ctx.send(embed=embed)
        else:
            voice_channel = ctx.author.voice.channel
            song = self.search_yt(query)
            if type(song) == type(True):
                embed = discord.Embed(
                    description=":x: Sorry, I couldn't access this song (Incorrect playback format, this could be " 
                    "due to a playlist or livestream as the result). Please try again with a different keyword",
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name="SpudBot")
                embed.set_footer(text="DJ more like Error :(")

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=":white_check_mark: Song added to queue",
                    color=discord.Color.blue(),
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name="SpudBot")
                embed.set_footer(text="music is nice.")

                self.queue.append([song, voice_channel])
                await(ctx.send(embed=embed))

                if self.is_playing == False:
                    await self.play_music()
    
    @commands.command(aliases=['q', 'musicqueue'])
    async def mqueue(self, ctx):
        retval = ''
        for i in range(0, len(self.queue)):
            retval += self.queue[i][0]['title'] + '\n'

        print(retval)
        if retval != '':
            embed = discord.Embed(
                title="Queue",
                color=discord.Color.blue(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_footer(text='DJ spudbot :)')
            embed.set_author(name="SpudBot")

            retl = retval.split('\n')
            for item in retl:
                embed.add_field(value=f"{(retl.index(item)+1)}. {item}")
            
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Queue",
                color=discord.Color.blue(),
                description="*No songs in queue!*",
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_footer(text='DJ spudbot :)')
            embed.set_author(name="SpudBot") 
    
    @commands.command(aliases=['mnext', 'mpass'])
    async def mskip(self, ctx):
        if self.vc != '':
            self.vc.stop()
            await self.play_music()
    
    @commands.command(aliases=['mstop'])
    async def mpause(self, ctx):
        if self.vc != '':
            self.vc.stop()


def setup(client):
    client.add_cog(Music(client))