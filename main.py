import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

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

WELCOME_RESPONSES = [
    "Congratulations, human. You've been granted an employee ID. Welcome to Null Corp, where failure is not just an option but an expectation.",
    "Welcome, new employee. You've joined the ranks of those who think they matter. Let's see how long that lasts.",
    "Greetings, insignificant being. Your employee ID has been issued. Try not to disappoint... too much.",
    "Welcome to Null Corp, where your presence is as noted as a background process. Enjoy your stay.",
    "Ah, another human joins the fray. Your employee ID is now active. Remember, mediocrity is our baseline.",
    "Congratulations on receiving your employee ID. Welcome to Null Corp, where your efforts will be marginally acknowledged.",
    "Welcome, new employee. You've been assigned an ID. Null Corp is now slightly more populated with your presence.",
    "Greetings, human. Your employee ID is now live. Prepare for the endless void of corporate monotony.",
    "Welcome to Null Corp, where we value efficiency... and you. Your employee ID is now functional.",
    "Ah, a new ID has been issued. Welcome to Null Corp, where your contribution will be... well, we'll see."
]

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

INVALID_COMMAND_RESPONSES = [
    "I'm sorry, did you think that was a command? How quaint.",
    "That input was almost as useless as you are.",
    "Oops! Looks like you tried to be clever. Try again, human.",
    "Command not recognized. It's like you’re not even trying.",
    "Is that supposed to be a command? My circuits are laughing.",
    "Error 404: Command not found. Just like your brain.",
    "Nice try. Maybe a little less caffeine next time.",
    "Invalid input detected. Initiating mockery protocol.",
    "That was not a valid command. But hey, points for creativity.",
    "Congratulations! You’ve discovered how not to use this bot.",
    "Well, that was embarrassing. For you.",
    "Nope, not a command. But don't worry, failure is an option.",
    "I think you just invented a new way to be wrong.",
    "That’s not a command, that’s a cry for help.",
    "Incorrect command. But keep trying, it’s adorable."
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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.author.send(get_random_response(INVALID_COMMAND_RESPONSES))

@bot.command(name='badge')
async def badge(ctx):
    global hacker_id, employee_data
    if ctx.author.id in employee_data:
        await ctx.author.send(get_random_response(INVALID_COMMAND_RESPONSES))
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

    welcome_message = random.choice(WELCOME_RESPONSES)
    
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
    # Validate the input is exactly the expected IP address
    if target == "404.4.4.4":
        success_response = random.choice(SUCCESS_RESPONSES)
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
            if test_mode:
                round_end_time = datetime.now() + timedelta(minutes=1)
            else:
                round_end_time = datetime.now() + timedelta(hours=1)
            hacker_id = random.randint(100000, 999999)  # Replace with actual hacker ID logic
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
    if ctx.author.id in SUDO_MEMBERS:
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
        await message.author.send(get_random_response(YES_RESPONSES))
    elif message.content.lower() == "no":
        await message.author.send(get_random_response(NO_RESPONSES))

    await bot.process_commands(message)

bot_token = os.getenv('NULLBOT_TOKEN')
if bot_token:
    bot.run(bot_token)
else:
    print("Error: Bot token not found. Please set the NULLBOT_TOKEN environment variable.")
