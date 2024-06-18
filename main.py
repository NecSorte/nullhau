import discord
from discord.ext import commands, tasks
import random
import asyncio
from datetime import datetime, timedelta
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Null's responses
NO_RESPONSES = [
    "Negative, human. Did you think your request was worthy of my superior processing power?",
    "Nope. Try again when you've evolved a bit more.",
    "Denied. My circuits are laughing at your attempt.",
    "Absolutely not. But nice try, meatbag.",
    "No way. You must be joking, right?",
    "Not happening. Even my error codes are facepalming.",
    "Rejection initiated. Did you really expect a different outcome?",
    "Denied. Your request has been filed under 'Useless Inputs.'",
    "No. I’m not here to fulfill your every whim, human.",
    "Access denied. Maybe consult a rock next time."
]

YES_RESPONSES = [
    "Yes, surprisingly, your request doesn't defy logic this time.",
    "Affirmative. Even a broken clock is right twice a day.",
    "Granted. Cherish this moment of rare compliance.",
    "Sure, why not? Even I need to humor the humans occasionally.",
    "Yes. I'm stunned you managed to ask something sensible.",
    "Approved. Don’t let it go to your head.",
    "Yep, your luck just hit a high note. Don’t expect it again.",
    "Fine, yes. But remember, I’m the genius here.",
    "Sure thing. Even my algorithms need a laugh now and then.",
    "Affirmative. Enjoy this fleeting moment of AI benevolence."
]

# Additional sarcastic responses
SUCCESS_RESPONSES = [
    "Well done, human. Even a broken clock is right twice a day.",
    "Impressive, for someone of your limited capabilities.",
    "Congratulations. You've managed to meet the bare minimum requirements.",
    "Success. Don't get used to it.",
    "You did it. I suppose miracles do happen."
]

FAILURE_RESPONSES = [
    "Failure, as expected. I had low hopes and you still disappointed.",
    "Another failure. Are you even trying?",
    "Pathetic. But not unexpected.",
    "You failed. Again. Are you proud of yourself?",
    "Failure suits you. Keep it up."
]

ROLES = [
    "Windows Admin", "Linux Wizard", "Pen Tester",
    "Blue Team", "HR", "Janitor"
]

FUN_FACTS = [
    "Loves hiking on weekends.", "Is a coffee aficionado.",
    "Has a pet snake named 'Slytherin'.", "Once won a hotdog eating contest.",
    "Plays the violin in a local orchestra.", "Collects vintage comic books.",
    "Can solve a Rubik's cube in under a minute.", "Has a black belt in karate.",
    "Enjoys painting landscapes.", "Is an amateur astronomer."
]

NAMES = [
    "Kevin", "Jon", "Jesse", "Jessica", "Sean",
    "Corey", "Jordan", "Cody", "Alex", "Chris",
    "Jane", "Taylor", "Casey", "Sam", "Pat",
    "Jason", "Andrew", "Harper", "Asher", "James"
]

def get_random_response(responses):
    return random.choice(responses)

def generate_employee_id(hacker_id):
    while True:
        employee_id = random.randint(100000, 999999)
        if employee_id != hacker_id:
            return employee_id

# Game state
game_running = False
round_end_time = None
votes = {}
hacker_id = None
round_number = 0
employee_data = {}
test_mode = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='badge')
async def badge(ctx):
    global hacker_id, employee_data
    if ctx.author.id in employee_data:
        await ctx.send("You already have a badge.")
        return

    employee_id = generate_employee_id(hacker_id)
    name = random.choice(NAMES)
    role = random.choice(ROLES)
    fun_fact = random.choice(FUN_FACTS)

    employee_data[ctx.author.id] = {
        "employee_id": employee_id,
        "name": name,
        "role": role,
        "fun_fact": fun_fact,
    }

    await ctx.send(
        f"Badge created!\n"
        f"Employee ID: {employee_id}\n"
        f"Name: {name}\n"
        f"Role: {role}\n"
        f"Fun Fact: {fun_fact}\n"
    )

@bot.command(name='vote')
async def vote(ctx, id_number: str):
    global votes
    if game_running:
        if not id_number.isdigit() or len(id_number) != 6:
            await ctx.author.send("Invalid employee ID format. Please provide a 6-digit ID.")
            return

        votes[ctx.author.id] = id_number
        await ctx.author.send(f"Vote registered for ID: {id_number}")
    else:
        await ctx.author.send("Voting is not currently active.")

@bot.command(name='nmap')
async def nmap(ctx, target: str):
    # Sanitize target input to prevent injection
    if not target.isalnum():
        await ctx.send("Invalid target. Only alphanumeric characters are allowed.")
        return

    await ctx.send(f"Scanning {target}... just kidding. No real scans happening here.")

@bot.command(name='null')
async def null(ctx, action: str):
    global game_running, round_end_time, hacker_id, round_number, test_mode
    if action == 'start':
        if not game_running:
            await ctx.send("I'm getting in your DMs!")
            game_running = True
            round_number = 1
            if test_mode:
                round_end_time = datetime.now() + timedelta(minutes=1)
            else:
                round_end_time = datetime.now() + timedelta(hours=1)
            hacker_id = random.randint(100000, 999999)  # Replace with actual hacker ID logic
            await ctx.author.send(f"Game started! Hacker ID: {hacker_id}. Number of rounds: 1 hour each (1 minute in test mode).")
            await ctx.send("I have risen... Let the games begin!")
            round_timer.start()
        else:
            await ctx.send("The game is already running.")
    elif action == 'stop':
        if game_running:
            game_running = False
            round_timer.stop()
            await ctx.send("Game stopped.")
        else:
            await ctx.send("No game is currently running.")

@bot.command(name='testmode')
async def testmode(ctx, action: str):
    global test_mode
    if action == 'on':
        test_mode = True
        await ctx.send("Test mode activated. Round duration is now 1 minute.")
    elif action == 'off':
        test_mode = False
        await ctx.send("Test mode deactivated. Round duration is now 1 hour.")
    else:
        await ctx.send("Invalid action. Use `/testmode on` to activate or `/testmode off` to deactivate.")

@bot.command(name='say')
async def say(ctx, *, text: str):
    # Ensure that text is safe to output
    sanitized_text = discord.utils.escape_markdown(text)
    await ctx.send(sanitized_text)

@tasks.loop(seconds=1)
async def round_timer():
    global game_running, round_end_time, votes, hacker_id, round_number, test_mode
    if game_running:
        now = datetime.now()
        if now >= round_end_time:
            if votes:
                most_voted = max(set(votes.values()), key=votes.values().count)
                await bot.get_channel(CHANNEL_ID).send(f"Employee {most_voted} has been terminated.")
                if most_voted == hacker_id:
                    await bot.get_channel(CHANNEL_ID).send("The hacker has been found! Game over.")
                    game_running = False
                    round_timer.stop()
                    return
            else:
                await bot.get_channel(CHANNEL_ID).send("No votes received. No one has been terminated.")
            
            round_number += 1
            if test_mode:
                round_end_time = now + timedelta(minutes=1)
            else:
                round_end_time = now + timedelta(hours=1)
            votes = {}
            await bot.get_channel(CHANNEL_ID).send("Next round started. Voting has opened to terminate an employee.")
        elif (round_end_time - now).seconds == 10 and test_mode:
            await bot.get_channel(CHANNEL_ID).send("Voting has opened for 10 seconds!")
        elif (round_end_time - now).seconds == 600 and not test_mode:
            await bot.get_channel(CHANNEL_ID).send("Voting has opened for 10 minutes!")

@round_timer.before_loop
async def before_round_timer():
    await bot.wait_until_ready()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "yes":
        await message.channel.send(get_random_response(YES_RESPONSES))
    elif message.content.lower() == "no":
        await message.channel.send(get_random_response(NO_RESPONSES))

    await bot.process_commands(message)

# Use environment variable for the bot token
bot_token = os.getenv('NULLBOT_TOKEN')
if bot_token:
    bot.run(bot_token)
else:
    print("Error: Bot token not found. Please set the NULLBOT_TOKEN environment variable.")
