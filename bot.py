import random
import discord
from discord.ext import commands,tasks
from discord.utils import get
import os
from itertools import cycle
import datetime
from discord.utils import get



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



youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)





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



client.run('ODA0Mzg3MjA3NDIyODA0MDA4.YBLl9w.8ZEzxE7Vzw57tjQcv52NHYBXQpM')
