import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
import logging
import asyncio
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from responses import NO_RESPONSES, YES_RESPONSES, WELCOME_RESPONSES, SUCCESS_RESPONSES, FAILURE_RESPONSES, INVALID_COMMAND_RESPONSES, TERMINATION_RESPONSES, WINDOWS_RESPONSES

# Load environment variables from .env file
load_dotenv()

TEST_MODE = os.getenv('TEST_MODE', 'off').lower() == 'on'

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

FUN_FACTS = [
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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
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
    fun_fact = random.choice(FUN_FACTS)

    employee_data[ctx.author.id] = {
        "employee_id": employee_id,
        "name": name,
        "role": role,
        "fun_fact": fun_fact,
    }

    welcome_message = get_random_welcome_response()
    
    await ctx.author.send(
        f"{welcome_message}\n"
        f"Badge created!\n"
        f"Employee ID: {employee_id}\n"
        f"Name: {name}\n"
        f"Role: {role}\n"
        f"Fun Fact: {fun_fact}\n"
    )

@bot.command(name='vote')
async def vote(ctx, id_number: str):
    global votes, vote_times
    if game_running:
        if not id_number.isdigit() or len(id_number) != 6:
            await ctx.author.send("Invalid employee ID format. Please provide a 6-digit ID.")
            return

        votes[ctx.author.id] = id_number
        vote_times[ctx.author.id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        termination_response = random.choice(TERMINATION_RESPONSES)
        await ctx.author.send(f"{termination_response}\nVote registered for ID: {id_number}")
    else:
        await ctx.author.send("Voting is not currently active.")

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
    global game_running, round_end_time, hacker_id, round_number, test_mode
    if action == 'start':
        if not game_running:
            await ctx.author.send("I'm getting in your DMs!")
            game_running = True
            round_number = 1
            if TEST_MODE:
                round_end_time = datetime.now() + timedelta(minutes=1)
                await ctx.author.send("Test mode activated. Game rounds will last 1 minute.")
            else:
                round_end_time = datetime.now() + timedelta(hours=1)
                await ctx.author.send("Game rounds will last 1 hour.")
            hacker_id = random.randint(100000, 999999)
            await ctx.author.send(f"Game started! Hacker ID: {hacker_id}.")
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
    global TEST_MODE
    if action == 'on':
        TEST_MODE = True
        await ctx.author.send("Test mode activated. All durations will be shortened.")
    elif action == 'off':
        TEST_MODE = False
        await ctx.author.send("Test mode deactivated. Durations will return to normal.")
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

async def automated_voting():
    global votes, vote_times
    if game_running:
        for member_id in employee_data.keys():
            target_id = str(random.randint(100000, 999999))
            votes[member_id] = target_id
            vote_times[member_id] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await bot.get_user(member_id).send(f"Automated vote registered for ID: {target_id}")
        await bot.get_channel(CHANNEL_ID).send("Automated voting completed.")

async def automated_nmap_scans():
    if game_running:
        await bot.get_channel(CHANNEL_ID).send("/nmap 404.4.4.4")
        await bot.get_channel(CHANNEL_ID).send("/nmap 192.168.1.1")

async def generate_summary_report():
    global votes, vote_times
    summary_report = "Test Mode Summary Report:\n\n"
    
    summary_report += "Votes:\n"
    for voter_id, voted_id in votes.items():
        vote_time = vote_times.get(voter_id, "Unknown time")
        summary_report += f"Voter ID: {voter_id} voted for {voted_id} at {vote_time}\n"
    
    summary_report += "\nGame State:\n"
    summary_report += f"Game Running: {game_running}\n"
    summary_report += f"Round Number: {round_number}\n"
    summary_report += f"Hacker ID: {hacker_id}\n"
    
    logging.info(summary_report)
    await bot.get_channel(CHANNEL_ID).send(f"```{summary_report}```")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def log_action(action):
    logging.debug(action)

@bot.event
async def on_command(ctx):
    log_action(f"Command executed: {ctx.command} by {ctx.author}")

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
        await message.author.send(get_random_yes_response())
    elif message.content.lower() == "no":
        await message.author.send(get_random_no_response())

    await bot.process_commands(message)

bot_token = os.getenv('NULLBOT_TOKEN')
if bot_token:
    bot.run(bot_token)
else:
    print("Error: Bot token not found. Please set the NULLBOT_TOKEN environment variable.")


