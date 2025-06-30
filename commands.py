"""
Additional commands for the CS2 bot.
Import this file to automatically register these commands.
"""

import sys

# Get the main module's register_command and send_message functions
if '__main__' in sys.modules:
    main_module = sys.modules['__main__']
    if hasattr(main_module, 'register_command'):
        register_command = main_module.register_command
        send_message = main_module.send_message
    else:
        from cs2bot import register_command, send_message
else:
    from cs2bot import register_command, send_message

import random
from datetime import datetime
from meows import get_random_meow

@register_command("meow", "Send a random meow")
def cmd_meow(username, team, args, team_chat):
    """Meow command"""
    meow_message = get_random_meow()
    send_message(f"{meow_message}", team_chat=team_chat)

@register_command("roll", "Roll a dice (1-6) or custom range")
def cmd_roll(username, team, args, team_chat):
    """Roll dice command"""
    import random
    
    if args:
        try:
            # Parse range like "1-20" or just "20"
            if '-' in args:
                min_val, max_val = map(int, args.split('-', 1))
            else:
                min_val, max_val = 1, int(args)
            
            if min_val >= max_val or min_val < 1 or max_val > 1000:
                send_message(f"{username}, invalid range! Use 1-1000", team_chat=team_chat)
                return
                
            result = random.randint(min_val, max_val)
            send_message(f"{username} rolled {result} (range: {min_val}-{max_val})", team_chat=team_chat)
        except ValueError:
            send_message(f"{username}, invalid format! Use '>roll 6' or '>roll 1-20'", team_chat=team_chat)
    else:
        result = random.randint(1, 6)
        send_message(f"{username} rolled {result} (1-6)", team_chat=team_chat)

@register_command("time", "Show current time for halley")
def cmd_time(username, team, args, team_chat):
    """Show current time"""
    now = datetime.now().strftime("%H:%M:%S")
    send_message(f"Current time: {now}", team_chat=team_chat)

@register_command("flip", "Flip a coin")
def cmd_flip(username, team, args, team_chat):
    """Flip a coin"""
    result = random.choice(["Heads", "Tails"])
    send_message(f"{username} flipped: {result}", team_chat=team_chat)

@register_command("8ball", "Ask the magic 8-ball a question")
def cmd_8ball(username, team, args, team_chat):
    """Magic 8-ball command"""
    responses = [
        "It is certain", "Reply hazy, try again", "Don't count on it",
        "It is decidedly so", "Ask again later", "My reply is no",
        "Without a doubt", "Better not tell you now", "My sources say no",
        "Yes definitely", "Cannot predict now", "Outlook not so good",
        "You may rely on it", "Concentrate and ask again", "Very doubtful",
        "As I see it, yes", "Most likely", "Outlook good",
        "Yes", "Signs point to yes"
    ]
    
    if args:
        response = random.choice(responses)
        send_message(response, team_chat=team_chat)
    else:
        send_message(f"{username}, ask me a question first!", team_chat=team_chat)

@register_command("math", "Calculate simple math expressions")
def cmd_math(username, team, args, team_chat):
    """Simple calculator command"""
    if not args:
        send_message(f"{username}, provide a math expression! (e.g., >math 2+2)", team_chat=team_chat)
        return
    
    try:
        # Only allow safe math operations
        allowed_chars = set("0123456789+-*/.()^ ")
        if not all(c in allowed_chars for c in args):
            send_message(f"{username}, only basic math operations allowed!", team_chat=team_chat)
            return
        
        # Evaluate the expression safely
        result = eval(args)
        send_message(f"{args} = {result}", team_chat=team_chat)
    except:
        send_message(f"{username}, invalid math expression!", team_chat=team_chat)

@register_command("say", "Make the bot say something")
def cmd_say(username, team, args, team_chat):
    """Say command - makes bot repeat a message"""
    if args:
        send_message(f"{args}", team_chat=False)
    else:
        send_message(f"{username}, tell me what to say!", team_chat=team_chat)

@register_command("paws", "Make the bot spam \"mmmggpfffff pawwwwsssss......\"")
def cmd_paws(username, team, args, team_chat):
    """Paws command - spam message"""
    spam_message = "mmmggpfffff pawwwwsssss......"
    if args:
        count = int(args)
        if count < 1 or count > 100:
            send_message(f"{username}, please use a number between 1 and 100!", team_chat=team_chat)
            return
        for _ in range(count):
            send_message(spam_message, team_chat=team_chat)
    else:
        send_message(spam_message, team_chat=team_chat)