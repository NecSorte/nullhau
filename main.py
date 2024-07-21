import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import asyncio  # Import asyncio module
from collections import defaultdict
from responses import NO_RESPONSES, YES_RESPONSES, WELCOME_RESPONSES, SUCCESS_RESPONSES, FAILURE_RESPONSES, INVALID_COMMAND_RESPONSES, TERMINATION_RESPONSES, WINDOWS_RESPONSES

# Load environment variables from .env file
load_dotenv()

# Setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True  # Enable if you need presence updates
intents.members = True    # Enable if you need member updates

# Bot setup
bot = commands.Bot(command_prefix='/', intents=intents)

# Define the channel ID for #DEFCON32
CHANNEL_ID = 1252438027880366191
SUDO_ROLE_NAME = "sudo"  # Define the sudo role name

ROLES = [
    "Windows Admin", "Linux Wizard", "Pen Tester",
    "Blue Team", "HR", "Janitor"
]

ROLE_FACTS = [
    "Loves hiking on weekends.", "Is a coffee aficionado.",
    "Has a pet snake named 'Slytherin'.", "Once won a hotdog eating contest.",
    "Plays the violin in a local orchestra.", "Collects vintage comic books.",
    "Can solve a Rubik's cube in under a minute.", "Has a black belt in karate.",
    "Enjoys painting landscapes.", "Is an amateur astronomer."
]

NAMES = [
    "Kevin", "Jon", "Jesse", "Jessica", "Sean",
    "Cory", "Jordan", "Cody", "Alex", "Chris",
    "Jane", "Taylor", "Casey", "Sam", "Pat",
    "Jason", "Andrew", "Harper", "Asher", "James"
]

# Track last command timestamps for spam protection
COMMAND_COOLDOWN = 5  # seconds
user_last_command_time = defaultdict(lambda: datetime.min)

async def is_on_cooldown(user_id):
    now = datetime.now()
    last_command_time = user_last_command_time[user_id]
    if (now - last_command_time).seconds < COMMAND_COOLDOWN:
        return True
    user_last_command_time[user_id] = now
    return False

def get_random_no_response():
    return random.choice(NO_RESPONSES)

def get_random_yes_response():
    return random.choice(YES_RESPONSES)

def get_random_welcome_response():
    return random.choice(WELCOME_RESPONSES)

def get_random_success_response():
    return random.choice(SUCCESS_RESPONSES)

def get_random_failure_response():
    return random.choice(FAILURE_RESPONSES)

def get_random_invalid_command_response():
    return random.choice(INVALID_COMMAND_RESPONSES)

def get_random_windows_response():
    return random.choice(WINDOWS_RESPONSES)

def generate_employee_id(hacker_id):
    while True:
        employee_id = random.randint(100000, 999999)
        if employee_id != hacker_id:
            return employee_id

# Game state
game_running = False
round_end_time = None
votes = {}
vote_times = {}  # Track vote times
hacker_id = None
round_number = 0
employee_data = {}
test_mode = False
voted_users = set()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.author.send(get_random_invalid_command_response())

@bot.command(name='badge')
async def badge(ctx):
    global hacker_id, employee_data
    if ctx.author.id in employee_data:
        await ctx.author.send(get_random_invalid_command_response())
        return

    employee_id = generate_employee_id(hacker_id)
    name = random.choice(NAMES)
    role = random.choice(ROLES)
    role_fact = random.choice(ROLE_FACTS)

    employee_data[ctx.author.id] = {
        "employee_id": employee_id,
        "name": name,
        "role": role,
        "role_fact": role_fact,
    }

    welcome_message = get_random_welcome_response()
    
    await ctx.author.send(
        f"{welcome_message}\n"
        f"Badge created!\n"
        f"Employee ID: {employee_id}\n"
        f"Name: {name}\n"
        f"Role: {role}\n"
        f"Role Fact: {role_fact}\n"
    )

@bot.command(name='vote')
async def vote(ctx, id_number: str):
    global votes, vote_times, voted_users
    if not game_running:
        await ctx.author.send("Voting is not currently active.")
        return
    
    if ctx.author.id not in employee_data:
        await ctx.author.send("You need to have an employee badge to vote. Use /badge to get one.")
        return

    if ctx.author.id in voted_users:
        await ctx.author.send("You have already voted this round.")
        return
    
    if not id_number.isdigit() or len(id_number) != 6:
        await ctx.author.send("Invalid employee ID format. Please provide a 6-digit ID.")
        return

    votes[ctx.author.id] = id_number
    vote_times[ctx.author.id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    voted_users.add(ctx.author.id)
    termination_response = random.choice(TERMINATION_RESPONSES)
    await ctx.author.send(f"{termination_response}\nVote registered for ID: {id_number}")

@bot.command(name='nmap')
async def nmap(ctx, target: str):
    # Validate the input is exactly the expected IP address
    if target == "404.4.4.4":
        success_response = random.choice(SUCCESS_RESPONSES)
        windows_response = random.choice(WINDOWS_RESPONSES)
        nmap_response = """

```
Host script results:
| smb-vuln-ms17-010:
| VULNERABLE:
| Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
| State: VULNERABLE
| IDs: CVE:CVE-2017-0143
| Risk factor: HIGH
| A critical remote code execution vulnerability exists in Microsoft SMBv1
| servers (ms17-010).
|
| Disclosure date: 2017-03-14
| References:
| https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
| https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|_ https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
```
        """
        await ctx.author.send(
            f"{nmap_response}\n\n"
            f"{success_response}\n"
            f"{windows_response}\n"
        "")
    else:
        # Send a random failure response if the input is not valid
        failure_response = random.choice(FAILURE_RESPONSES)
        await ctx.author.send(failure_response)

@bot.command(name='null')
async def null(ctx, action: str):
    global game_running, round_end_time, hacker_id, round_number, test_mode, voted_users
    if action == 'start':
        if not game_running:
            await ctx.author.send("I'm getting in your DMs!")
            game_running = True
            round_number = 1
            if test_mode:
                round_end_time = datetime.now() + timedelta(minutes=1)
                await automated_voting()
                await automated_nmap_scans()
            else:
                round_end_time = datetime.now() + timedelta(hours=1)
            hacker_id = random.randint(100000, 999999)
            await ctx.author.send(f"Game started! Hacker ID: {hacker_id}. Number of rounds: 1 hour each (1 minute in test mode).")
            await ctx.author.send("Null is watching... Let the games begin!")
            round_timer.start()
        else:
            await ctx.author.send("The game is already running.")
    elif action == 'stop':
        if game_running:
            game_running = False
            round_timer.stop()
            await ctx.author.send("Game stopped.")
        else:
            await ctx.author.send("No game is currently running.")

@bot.command(name='testmode')
async def testmode(ctx, action: str):
    global test_mode
    if action == 'on':
        test_mode = True
        await ctx.author.send("Test mode activated. Round duration is now 1 minute.")
    elif action == 'off':
        test_mode = False
        await ctx.author.send("Test mode deactivated. Round duration is now 1 hour.")
    else:
        await ctx.author.send("Invalid action. Use `/testmode on` to activate or `/testmode off` to deactivate.")

@bot.command(name='say')
async def say(ctx, *, text: str):
    # Check if the author is a sudo member
    guild = ctx.guild
    sudo_role = discord.utils.get(guild.roles, name=SUDO_ROLE_NAME)
    if sudo_role in ctx.author.roles:
        # Sanitize the text to prevent injection attacks
        sanitized_text = discord.utils.escape_markdown(text)
        
        # Get the channel object
        channel = bot.get_channel(CHANNEL_ID)
        
        if channel is not None:
            # Send the sanitized message to the specified channel
            await channel.send(sanitized_text)
        else:
            await ctx.author.send("I couldn't find the channel to send the message to.")
    else:
        await ctx.author.send("You do not have permission to use this command.")

@bot.command(name='commands')
async def commands(ctx):
    help_text = (
        "Here are the commands you can use:\n"
        "/badge - Get your employee badge.\n"
        "/vote <id_number> - Vote to eliminate an employee by their ID.\n"
        "/nmap <target> - Simulate an nmap scan on a target (just for fun).\n"
        "/null <start|stop> - Start or stop the hacker game.\n"
        "/testmode <on|off> - Activate or deactivate test mode.\n"
        "/say <text> - Make the bot say something.\n"
        "/commands - Show this help message."
    )
    await ctx.author.send(help_text)

async def send_voting_statistics():
    global votes, vote_times
    
    # Get the guild (server) object. Replace CHANNEL_ID with your actual guild ID if necessary.
    guild = bot.get_guild(CHANNEL_ID)  # This should be your guild ID, not channel ID.

    if guild is None:
        print("Guild not found.")
        return

    # Get the sudo role
    sudo_role = discord.utils.get(guild.roles, name=SUDO_ROLE_NAME)
    
    if sudo_role is None:
        print("Sudo role not found.")
        return

    # Construct the statistics message
    statistics_message = "Voting Statistics:\n\n"
    
    for voter_id, voted_id in votes.items():
        vote_time = vote_times.get(voter_id, "Unknown time")
        voter_member = guild.get_member(voter_id)
        voter_name = voter_member.display_name if voter_member else "Unknown voter"
        statistics_message += f"{voter_name} (ID: {voter_id}) voted for {voted_id} at {vote_time}\n"
    
    hacker_voters = [voter for voter, voted in votes.items() if voted == hacker_id]
    statistics_message += "\nMembers who voted for the hacker:\n"
    for voter in hacker_voters:
        voter_member = guild.get_member(voter)
        voter_name = voter_member.display_name if voter_member else "Unknown voter"
        statistics_message += f"{voter_name} (ID: {voter})\n"

    # Send the message to all members with the sudo role
    for member in guild.members:
        if sudo_role in member.roles:
            try:
                await member.send(statistics_message)
            except discord.Forbidden:
                print(f"Could not send message to {member.display_name}")

@tasks.loop(seconds=1)
async def round_timer():
    global game_running, round_end_time, votes, hacker_id, round_number, test_mode, voted_users
    if game_running:
        now = datetime.now()
        if now >= round_end_time:
            if votes:
                most_voted = max(set(votes.values()), key=list(votes.values()).count)
                await bot.get_channel(CHANNEL_ID).send(f"Employee {most_voted} has been terminated.")
                if most_voted == hacker_id:
                    await bot.get_channel(CHANNEL_ID).send("The hacker has been found! Game over.")
                    game_running = False
                    round_timer.stop()
                    await send_voting_statistics()  # Send statistics to sudo members
                    return
            else:
                await bot.get_channel(CHANNEL_ID).send("No votes received. No one has been terminated.")
            
            round_number += 1
            if test_mode:
                round_end_time = now + timedelta(minutes=1)
            else:
                round_end_time = now + timedelta(hours=1)
            votes = {}
            vote_times = {}
            voted_users = set()
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

    if await is_on_cooldown(message.author.id):
        await message.channel.send("You are sending commands too quickly. Please wait a few seconds.")
        return

    if message.content.lower() == "yes":
        await message.author.send(get_random_yes_response())
    elif message.content.lower() == "no":
        await message.author.send(get_random_no_response())

    await bot.process_commands(message)

async def automated_voting():
    while game_running and test_mode:
        # Simulate a random user casting a vote
        random_user_id = random.choice(list(employee_data.keys()))
        random_vote = random.choice(list(employee_data.values()))['employee_id']
        votes[random_user_id] = random_vote
        vote_times[random_user_id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await asyncio.sleep(10)  # Adjust the interval for automated voting as needed

async def automated_nmap_scans():
    while game_running and test_mode:
        # Simulate a random nmap scan
        random_user_id = random.choice(list(employee_data.keys()))
        await nmap(bot.get_context(random_user_id), target="404.4.4.4")
        await asyncio.sleep(15)  # Adjust the interval for automated nmap scans as needed

bot_token = os.getenv('NULLBOT_TOKEN')
if bot_token:
    bot.run(bot_token)
else:
    print("Error: Bot token not found. Please set the NULLBOT_TOKEN environment variable.")
