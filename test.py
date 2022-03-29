import discord
from discord.ext import commands
import requests
import asyncio
import json
import psutil
import datetime
import os

# setuop our bot
bot = commands.Bot(command_prefix=',')


# create ready event
@bot.event
async def on_ready():
    # create a list of statuses to cycle through
    statuses = [
        f'Watching {len(bot.users)} users',
        'Made with Love',
        'In Floppa We Trust',
    ]
    # cycle through statuses
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# remove default help command
bot.remove_command('help')

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

# create a command if the user runs it, they get a media ping role, and if they already have the role but run it again, remove the role
@bot.command()
async def media(ctx):
    try:
        # get the role
        role = discord.utils.get(ctx.guild.roles, name='Media')
        # get the member
        member = ctx.message.author
        # check if the member has the role
        if role in member.roles:
            # remove the role
            await member.remove_roles(role)
            # send a message
            em = discord.Embed(description = f'{ctx.author.mention}, Removed the Media role.', color = 0xd30059)
            await ctx.send(embed = em)
        else:
            # add the role
            await member.add_roles(role)
            # send a message
            em = discord.Embed(description = f'{ctx.author.mention}, Added the Media role.', color = 0xd30059)
            await ctx.send(embed = em)
    except Exception as e:
        await ctx.send(f'{e}')

# create a command to lock a channel
@bot.command()
async def lock(ctx, *, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    ovrite = channel.overwrites_for(ctx.guild.default_role)
    ovrite.send_messages = False
    if channel == None:
        # check if the channel is already locked
        if channel.overwrites_for(ctx.guild.default_role).send_messages == False:
            # send a message
            em = discord.Embed(description = f'{ctx.author.mention}**, The channel is already locked.**', color = 0xd30059)
            await ctx.send(embed = em)
        else:
            await channel.set_permissions(ctx.guild.default_role, overwrite = ovrite)
            em = discord.Embed(description=f':lock: **<#{channel.id}> has been locked.**', color = 0xd30059)
            await ctx.send(embed = em)
    else:
        # check if the channel is already locked
        if channel.overwrites_for(ctx.guild.default_role).send_messages == False:
            # send a message
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
        # check if the channel is already unlocked
        if channel.overwrites_for(ctx.guild.default_role).send_messages == True:
            # send a message
            em = discord.Embed(description = f'{ctx.author.mention}**, The channel is already unlocked.**', color = 0xd30059)
            await ctx.send(embed = em)
        else:
            await channel.set_permissions(ctx.guild.default_role, overwrite = ovrite)
            em = discord.Embed(description=f':unlock: **<#{channel.id}> has been unlocked.**', color = 0xd30059)
            await ctx.send(embed = em)
    else:
        # check if the channel is already unlocked
        if channel.overwrites_for(ctx.guild.default_role).send_messages == True:
            # send a message
            em = discord.Embed(description = f'{ctx.author.mention}**, The channel is already unlocked.**', color = 0xd30059)
            await ctx.send(embed = em)
        else:
            await channel.set_permissions(ctx.guild.default_role, overwrite = ovrite)
            em = discord.Embed(description=f':unlock: **<#{channel.id}> has been unlocked.**', color = 0xd30059)
            await ctx.send(embed = em)

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

# login to bot
bot.run('')