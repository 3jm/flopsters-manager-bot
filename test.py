import discord
from discord.ext import commands
import requests
import asyncio
import json
import psutil
import datetime
import random
import datetime
from datetime import datetime
import os

bot = commands.Bot(command_prefix=',')

@bot.event
async def on_ready():
    statuses = [
        f'Watching {len(bot.users)} users',
        'Made with Love',
        'In Floppa We Trust',
    ]
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        description = f'commands with <> are required\ncommands with [] are optional',
        colour=discord.Colour.blue()
    )
    embed.set_author(name=f'Floppsters Help Menu', icon_url=f'{ctx.author.avatar_url}')
    embed.set_footer(text=f'{ctx.author.name} ({ctx.author.id})', icon_url=f'{ctx.author.avatar_url}')
    embed.timestamp = datetime.utcnow()
    embed.set_thumbnail(url=f'{bot.user.avatar_url}')
    embed.set_image(url='https://splashcord.com/wp-content/uploads/buddypress/groups/36/cover-image/623ab59542212-bp-cover-image.png')
    embed.add_field(name='Community Commands', value='`art`,`help`,`ping`,`media`,`,floppa`,`,sogga`', inline=False)
    embed.add_field(name='Moderation Commands', value='`kick <user>`,`ban <user> <reason>`\n`unban <user>`,`lock [channel]`\n`unlock [channel]`,`softban <user> <reason>`', inline=False)
    embed.add_field(name='Contribution', value='My source code is available on [GitHub](https://github.com/3jm/flopsters-manager-bot)', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def art(ctx):
    try:
        em = discord.Embed(
            title = f'Floppsters - Greatest Game of All Time',
            description = 'Get all the exclusive content from the [Floppsters Splashcord!](https://splashcord.com/groups/floppsters-greatest-game-of-all-time/)',
            color = 0xd30059
        )
        em.set_image(url='https://splashcord.com/wp-content/uploads/buddypress/groups/36/cover-image/623ab59542212-bp-cover-image.png')
        await ctx.send(embed = em)
    except Exception as e:
        await ctx.send(f'{e}')

Verified_Guilds= [954974341504831539]

@bot.command()
async def media(ctx):
    if ctx.guild.id not in Verified_Guilds:
        await ctx.send('This command is only available in Floppsters! You can join here\nhttps://discord.gg/cVJZhZQjhF')
        return
    try:
        role = discord.utils.get(ctx.guild.roles, name='Media')
        member = ctx.message.author
        if role in member.roles:
            await member.remove_roles(role)
            em = discord.Embed(description = f'{ctx.author.mention}, Removed the Media role.', color = 0xd30059)
            await ctx.send(embed = em)
        else:
            await member.add_roles(role)
            em = discord.Embed(description = f'{ctx.author.mention}, Added the Media role.', color = 0xd30059)
            await ctx.send(embed = em)
    except Exception as e:
        await ctx.send(f'{e}')

@bot.command()
async def lock(ctx, *, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    ovrite = channel.overwrites_for(ctx.guild.default_role)
    ovrite.send_messages = False
    if channel == None:
        if channel.overwrites_for(ctx.guild.default_role).send_messages == False:
            em = discord.Embed(description = f'{ctx.author.mention}**, The channel is already locked.**', color = 0xd30059)
            await ctx.send(embed = em)
        else:
            await channel.set_permissions(ctx.guild.default_role, overwrite = ovrite)
            em = discord.Embed(description=f':lock: **<#{channel.id}> has been locked.**', color = 0xd30059)
            await ctx.send(embed = em)
    else:
        if channel.overwrites_for(ctx.guild.default_role).send_messages == False:
            em = discord.Embed(description = f'{ctx.author.mention}**, The channel is already locked.**', color = 0xd30059)
            await ctx.send(embed = em)
        else:
            await channel.set_permissions(ctx.guild.default_role, overwrite = ovrite)
            em = discord.Embed(description=f':lock: **<#{channel.id}> has been locked.**', color = 0xd30059)
            await ctx.send(embed = em)

@bot.command()
async def unlock(ctx, *, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    ovrite = channel.overwrites_for(ctx.guild.default_role)
    ovrite.send_messages = True
    if channel == None:
        if channel.overwrites_for(ctx.guild.default_role).send_messages == True:
            em = discord.Embed(description = f'{ctx.author.mention}**, The channel is already unlocked.**', color = 0xd30059)
            await ctx.send(embed = em)
        else:
            await channel.set_permissions(ctx.guild.default_role, overwrite = ovrite)
            em = discord.Embed(description=f':unlock: **<#{channel.id}> has been unlocked.**', color = 0xd30059)
            await ctx.send(embed = em)
    else:
        if channel.overwrites_for(ctx.guild.default_role).send_messages == True:
            em = discord.Embed(description = f'{ctx.author.mention}**, The channel is already unlocked.**', color = 0xd30059)
            await ctx.send(embed = em)
        else:
            await channel.set_permissions(ctx.guild.default_role, overwrite = ovrite)
            em = discord.Embed(description=f':unlock: **<#{channel.id}> has been unlocked.**', color = 0xd30059)
            await ctx.send(embed = em)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    try:
        if ctx.author.guild_permissions.ban_members == True:
            await member.ban(reason=reason)
            await ctx.send(':thumbsup:')
        else:
            await ctx.send(':thumbsdown:')
    except Exception as e:
        print(f'Error: {e}')

@bot.command()
async def unban(ctx, *, member):
    try:
        if ctx.author.guild_permissions.ban_members == True:
            banned_users = await ctx.guild.bans()
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == member.split('#'):
                    await ctx.guild.unban(user)
                    await ctx.send(':thumbsup:')
                    return
        await ctx.send(':thumbsdown:')
    except Exception as e:
        print(f'Error: {e}')

@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    try:
        if ctx.author.guild_permissions.kick_members == True:
            await member.kick(reason=reason)
            await ctx.send(':thumbsup:')
        else:
            await ctx.send(':thumbsdown:')
    except Exception as e:
        print(f'Error: {e}')

@bot.command()
async def softban(ctx, member : discord.Member, *, reason=None):
    try:
        if ctx.author.guild_permissions.ban_members == True:
            await member.ban(reason=reason)
            await ctx.guild.unban(member)
            await ctx.send(':thumbsup:')
        else:
            await ctx.send(':thumbsdown:')
    except Exception as e:
        print(f'Error: {e}')


@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send(f'Discord: {round(bot.latency * 1000)}ms')

@bot.event
async def on_guild_join(guild):
    with open('db.json', 'r') as f:
        db = json.load(f)
    if str(guild.id) in db:
        pass
    else:
        name = guild.name
        id = guild.id
        db[str(id)] = {
            'name': name,
            'id': id
        }
    with open('db.json', 'w') as f:
        json.dump(db, f, indent=4)

@bot.command()
async def floppa(ctx):
    msg = await ctx.send('1 second please...')
    api = 'https://api.tenor.com/v1/search?q=floppa&key=LIVDSRZULELA&limit=50'
    data = requests.get(api).json()
    image = random.choice(data['results'])
    url = image['media'][0]['gif']['url']
    await msg.edit(content=url)

@bot.command()
async def sogga(ctx):
    msg = await ctx.send('1 second please...')
    api = 'https://api.tenor.com/v1/search?q=sogga&key=LIVDSRZULELA&limit=50'
    data = requests.get(api).json()
    image = random.choice(data['results'])
    url = image['media'][0]['gif']['url']
    await msg.edit(content=url)

bot.run('')