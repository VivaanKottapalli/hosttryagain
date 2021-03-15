import random
import discord
from discord.ext import commands,tasks
from discord.utils import get
import os
from itertools import cycle
import datetime
from discord.utils import get
import requests


def get_prefix(client,message):
    with open("prefix.json" , 'r') as f:
        prefixes = json.load(f)
        return prefixes[str(message.guild.id)]
client = commands.Bot(command_prefix= get_prefix)
client.remove_command('help')



    



players = {}

client = commands.Bot(command_prefix= 'e/')
client.remove_command('help')
    
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Watching over Not Rohan Twitch Server'))



@client.command()
async def help(ctx):
    embed=discord.Embed(title="Not Rohan!", description="------------------------------------", color=0xffff)
    embed.set_author(name="Not Rohan Bot commands")
    embed.add_field(name="`e/info`", value="The developers of the bot", inline=False)
    embed.add_field(name="`e/moderation`", value="TO VIEW THE MODERATION COMMANDS", inline=False)
    embed.add_field(name="`e/music`", value="TO VIEW THE MUSIC COMMANDS", inline=False)
    await ctx.send(embed=embed)




@client.command()
async def moderation(ctx):
    embed=discord.Embed(title="Bot's moderation commands", description="------------------------------------", color=0xffff)
    embed.set_author(name="moderation Commands")
    embed.add_field(name="`e/kick`", value="ban a member", inline=False)
    embed.add_field(name="`e/ban (your question)`", value="ban a member", inline=False)
    embed.add_field(name="`e/mute`", value="mute a member", inline=False)
    embed.add_field(name="e/unmute", value="to unmute", inline=False)
    embed.add_field(name="e/purge", value="to remove text", inline=False)
    await ctx.send(embed=embed)


@client.command()
async def info(ctx):
    embed=discord.Embed(title="Bot's info", description="------------------------------------", color=0xffff)
    embed.set_author(name="moderation Commands")
    embed.add_field(name="`People who made this bot`", value="Vivgang(Wewaan) has developed this bot for Not Rohan's discord server", inline=False)
    await ctx.send(embed=embed)






@client.command()
@commands.has_permissions(kick_members=True)
async def purge(ctx, amount=0):
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(title="Purge", description=f"{amount} messages have been purged", color=0xfbff00)
        await ctx.send(embed=embed)

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Sorry you are not allowed to use this command.')




@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member = None):
    if not member:
        embed = discord.Embed(title="Kicking a  member", description="specify a member to kick", color=0xfbff00)
        await ctx.send(embed=embed)
        return
    await member.kick()
    embed = discord.Embed(title="Kicking a member", description=f"{member.mention} has been kicked. BEGONE THOT", color=0xfbff00)
    await member.send(f"You were KICKED in the server {ctx.guild.name}")
    await ctx.send(embed=embed)
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title="Kicking a member", description="You dont have perms you know", color=0xfbff00)
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member = None):
    if not member:
        embed = discord.Embed(title="Kicking a member", description="You dont have perms you know", color=0xfbff00)
        await ctx.send(embed=embed)
        return
    await member.ban()
    embed = discord.Embed(title="Banning a member", description="GET OUT BITCH", color=0xfbff00)
    await member.send(f"You were BANNED in the server {ctx.guild.name}")
    await ctx.send(embed=embed)
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title="Kicking a member", description="BRUH MOMENTO, YOU NEED PERMS LOL", color=0xfbff00)
        await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member=None):
    if not member:
        embed = discord.Embed(title="mute a member", description=f"Bruh tell me who.", color=0xfbff00)
        await ctx.send(embed=embed)
        return
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.add_roles(role)
    embed = discord.Embed(title="mute a member", description=f"{member.mention} has been muted. SHUT UP", color=0xfbff00)
    await member.send(f"You were muted in the server {ctx.guild.name}")
    role = discord.utils.get(ctx.guild.roles, name="access")
    await member.remove_roles(role)
    await ctx.send(embed=embed)
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        emrwe = discord.Embed(title = "You cant mute!", description= member.mention, color=0xfbff00)


@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    role = discord.utils.get(ctx.guild.roles, name='access')
    await ctx.send(f"Unmuted {member.mention}")
    await member.add_roles(role)
    await member.send(f"You were unmuted in the server {ctx.guild.name}")



@client.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member=None, reason = None):
    await ctx.send(f"Warned {member.mention} for {reason}")
    await member.send(f"You were warned in the Not Rohan's server for {reason}")
    
@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


@client.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")


@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@client.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")


queues = {}

@client.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])
    await ctx.send("Adding song " + str(q_num) + " to the queue")

    print("Song added to queue\n")



@client.command()
async def userinfo(ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        roles = [role for role in member.roles]

        embed = discord.Embed(color=member.color, timestamp=datetime.datetime.utcnow())

        embed.set_author(name=f"{member}", icon_url=member.avatar_url)

        embed.set_image(url=member.avatar_url)

        embed.add_field(name="Joined at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))

        embed.add_field(name="Top role:", value=member.top_role.mention)
        embed.set_footer(text=f"Requested By: {ctx.author.name}")

        await ctx.send(embed=embed)







@client.command()
async def membercount(ctx):
    mbed = discord.Embed(
        color=discord.Color(0xffff),
        title=f"{ctx.guild.name}"
    )
    mbed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    mbed.add_field(name='Membed Count', value=f"{ctx.guild.member_count}")
    mbed.set_footer(icon_url=f"{ctx.guild.icon_url}", text=f"Server ID: {ctx.guild.id}")
    await ctx.send(embed=mbed)



@client.command(aliases=['av'])
async def avatar(ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        embed = discord.Embed(color=member.color, timestamp=datetime.datetime.utcnow())

        embed.set_author(name=f"{member}", icon_url=member.avatar_url)

        embed.set_image(url=member.avatar_url)

        await ctx.send(embed=embed)


@client.command()
async def announce(ctx, channel: discord.TextChannel, *, msg):
    await ctx.send('Sent message!')
    await channel.send(f'{msg}')

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong!{round(client.latency * 1000)}ms")


@client.command()
async def server(ctx):
    r = requests.get(r = requests.get('https://api.minehut.com/server/c0ba1t?byName=true'))
    json_data =  r.json
    print(json_data)
    description = json_data["server"]["motd"]
    online = str(json_data["server"]["online"])
    playercount = str(json_data["server"]["playercount"])

    embed = discord.Embed(
        title="c0ba1t sever info",
        description='Description: ' + description + 'n/Online Status:' + online + '/nPlayers Online: ' + playercount,
        color= discord.Color.purple()
    )
    await ctx.send(embed=embed)



client.run('ODA0Mzg3MjA3NDIyODA0MDA4.YBLl9w.8ZEzxE7Vzw57tjQcv52NHYBXQpM')
