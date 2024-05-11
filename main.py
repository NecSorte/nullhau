import discord
from discord.ext import commands, tasks
import asyncio
from collections import defaultdict
import random

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No bot token found in the environment variables!")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Game state storage
votes = defaultdict(int)
voting_channel_id = None
game_master_id = None
assigned_ids = {}
hacker_id = None

# Command to assign the game master
@bot.command()
async def hacker(ctx):
    global game_master_id
    if game_master_id is not None:
        await ctx.send("A game master is already set!")
        return
    
    game_master_id = ctx.author.id
    await ctx.author.send("You are the SUDO Game Master. Type 'random', 'debug', or a specific six-digit ID.")
    await ctx.send("A hacker is among us!")

# Command to receive ID
@bot.command()
async def id(ctx):
    if ctx.author.id in assigned_ids:
        await ctx.author.send("You already have an ID.")
        return
    
    new_id = random.randint(100000, 999999)
    while new_id in assigned_ids:
        new_id = random.randint(100000, 999999)
    assigned_ids.append(new_id)
    await ctx.author.send(f"Your ID is {new_id}")

# DM listener for the game master
@bot.listen('on_message')
async def on_message(message):
    if message.author.id == game_master_id and isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == 'random':
            global hacker_id
            hacker_id = random.choice(assigned_ids)
        elif message.content.isdigit() and len(message.content) == 6:
            hacker_id = int(message.content)
        else:
            return

        await bot.get_channel(origin_channel_id).send(f"Message from Null: {message.content}")


# Periodic check for ending voting and announcing results
@tasks.loop(hours=1)
async def hourly_vote_check():
    global votes
    if not votes:
        return
    # Determine the most voted ID
    max_votes = max(votes.values())
    suspects = [id for id, count in votes.items() if count == max_votes]
    channel = bot.get_channel(voting_channel_id)
    for suspect in suspects:
        await channel.send(f"Eliminating employee ID: {suspect} — My algorithms find your trust factor dubious.")
    votes.clear()  # Reset votes for the next round

# Start the loop when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    hourly_vote_check.start()  

@bot.command()
async def start(ctx):
    global voting_channel_id, game_master_id
    if game_master_id:  # Ensure only one game master can initiate the game
        await ctx.send("A game is already in progress.")
        return
    game_master_id = ctx.author.id
    voting_channel_id = ctx.channel.id
    await ctx.send("Game initialized. Begin your deductions, humans. My circuits are watching.")

@bot.command()
async def vote(ctx, employee_id: str):
    if ctx.author.id in assigned_ids and assigned_ids[ctx.author.id] != employee_id:
        votes[employee_id] += 1
        await ctx.author.send(f"Your vote for ID {employee_id} has been registered. Let's see if you're as smart as you believe.")
    else:
        await ctx.author.send("You cannot vote for yourself or an invalid Employee ID.")

@bot.command()
async def assign_hacker(ctx, method: str):
    if ctx.author.id != game_master_id:
        await ctx.send("You are not the game master.")
        return
    if method.lower() == "random":
        global hacker_id
        hacker_id = random.choice(list(assigned_ids.values()))
        await ctx.send("A hacker has been randomly assigned.")
    elif method.isdigit() and len(method) == 6:
        hacker_id = method
        await ctx.send(f"Hacker has been assigned with Employee ID {method}.")

@bot.command()
async def register(ctx):
    if ctx.author.id in assigned_ids:
        await ctx.author.send("You already have an ID.")
        return
    new_id = random.randint(100000, 999999)
    while new_id in assigned_ids.values():
        new_id = random.randint(100000, 999999)
    assigned_ids[ctx.author.id] = new_id
    await ctx.author.send(f"Your Employee ID for this game is {new_id}")

# Run the bot
bot.run('DISCORD_BOT_TOKEN')
