import re
import asyncio
import globals
import pydirectinput
import pyautogui
from time import sleep

# CS2 chat regex pattern - matches: [TEAM] username‎location [DEAD]: !command args
CS2_REGEX = r"\[(?P<team>ALL|CT|T)\]\s+(?P<username>.*)‎(?:﹫(?P<location>.*?))?\s*(?P<dead_status>\[DEAD\])?:\s*(?P<command>\S+)?\s*(?P<args>.*)?"

# Command registry - stores command functions
COMMANDS = {}

def register_command(name, description=""):
    """Register a command function"""
    def decorator(func):
        full_name = f"{globals.COMMAND_PREFIX}{name}"
        COMMANDS[full_name] = {
            'func': func,
            'description': description
        }
        return func
    return decorator

@register_command("help", "Show available commands")
def cmd_help(username, team, args, team_chat):
    """Help command - shows all available commands"""
    if args:
        # Show help for specific command
        cmd_name = f"{globals.COMMAND_PREFIX}{args}"
        if cmd_name in COMMANDS:
            desc = COMMANDS[cmd_name]['description']
            send_message(f"{cmd_name}: {desc}", team_chat=team_chat)
        else:
            send_message(f"Command '{args}' not found.", team_chat=team_chat)
    else:
        # Show all commands
        cmd_names = [cmd.replace(globals.COMMAND_PREFIX, "") for cmd in COMMANDS.keys()]
        send_message(f"Commands: {', '.join(cmd_names)}", team_chat=team_chat)

show_debug = globals.VERBOSE  # Use global verbose setting

# Template generator for safe command execution (simplified for CS2)
class TemplateGenerator:
    def __init__(self):
        pass

    def generate(self, command):
        # Execute command directly without aliases to avoid caching issues
        return f'{command}\n'

gen = TemplateGenerator()

last_line = ""

commands_out_of_focus = []

def tail_log():
    """Read the last line of console.log"""
    try:
        with open(globals.LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            if lines:
                return lines[-1].strip()
    except FileNotFoundError:
        print(f"[Error] Console log file not found: {globals.LOG_FILE}")
    except Exception as e:
        print(f"[Error] Reading log file: {e}")
    return ""

def parse_chat_line(line):
    """Parse a chat line using CS2 regex pattern"""
    # Skip lines that contain our bot's prefix to avoid processing our own messages
    if globals.PREFIX in line:
        return None
    
    # Skip InputService lines (these are from command execution)
    if "[InputService]" in line:
        return None
        
    regex = re.search(CS2_REGEX, line, flags=re.UNICODE | re.VERBOSE)
    if regex:
        team = regex.group("team")
        username = regex.group("username").replace(";", ":") if regex.group("username") else ""
        location = regex.group("location")
        dead_status = regex.group("dead_status")
        command = regex.group("command").replace(";", ":") if regex.group("command") else ""
        args = regex.group("args").replace(";", ":") if regex.group("args") else ""
        
        return {
            'team': team,
            'username': username,
            'location': location,
            'dead': dead_status,
            'command': command,
            'args': args
        }
    return None

def is_valid_command(command):
    """Check if the command is in our command registry"""
    return command and command in COMMANDS

def execute_command(command):
    """Execute a command by writing it to the cfg file using template generator"""
    try:
        with open(globals.CFG_FILE, 'w', encoding='utf-8') as f:
            templated_command = gen.generate(command)
            f.write(templated_command)
            
            if show_debug:
                print(f"[Debug] Title: {pyautogui.getActiveWindowTitle()}")  # Debug output

        # wait for file to be written
        sleep(0.5)

        # Check if CS2 is focused
        if pyautogui.getActiveWindowTitle() != "Counter-Strike 2":
            print(f"[Warn] Counter-Strike 2 is not focused, command not executed.")
            commands_out_of_focus.append(command)
        else:
            pydirectinput.press('n')
            if show_debug:
                print(f"[Debug] Pressed 'n' to execute command: {command}")
    except Exception as e:
        print(f"[Error] Failed to execute command: {e}")

def send_message(msg, team_chat=False):
    """Send a message to chat"""
    command = ""
    if team_chat:
        command = f'say_team "{globals.PREFIX} {msg}"'
    else:
        command = f'say "{globals.PREFIX} {msg}"'
    execute_command(command)

# Import additional commands after the core functions are defined
try:
    import commands
    print(f"[CS2 ChatBot] Loaded additional commands from commands.py")
except ImportError as e:
    print(f"[CS2 ChatBot] Could not load commands.py: {e}")
except Exception as e:
    print(f"[CS2 ChatBot] Error loading commands.py: {e}")

def process_command(chat_data):
    """Process a parsed command immediately"""
    command = chat_data['command'].lower()
    args = chat_data['args']
    username = chat_data['username']
    team = chat_data['team']
    
    print(f"[Command] {username} ({team}): {command} {args}")
    
    if show_debug:
        print(f"[Debug] Processing command immediately: {command} by {username} on team {team}")
    
    # Process command immediately instead of queuing
    handle_command_immediate(chat_data)

def handle_command_immediate(chat_data):
    """Process a single command immediately"""
    command = chat_data['command']
    username = chat_data['username']
    team = chat_data['team']
    args = chat_data['args'].strip() if chat_data['args'] else ""

    if show_debug:
        print(f"[Debug] Handling command: {command} from {username} on team {team} with args: '{args}'")
    
    # Only respond to players on valid teams
    if team not in ['CT', 'T', 'ALL']:
        return
    
    # Determine if this should be team chat
    team_chat = team in ['CT', 'T']

    # Execute command if it exists in registry
    if command in COMMANDS:
        try:
            COMMANDS[command]['func'](username, team, args, team_chat)
        except Exception as e:
            print(f"[Error] Command {command} failed: {e}")
            send_message(f"Sorry {username}, command failed!", team_chat=team_chat)
    else:
        if show_debug:
            print(f"[Debug] Unknown command: {command}")

def handle_out_of_focus_commands():
    """Handle commands that were executed while CS2 was out of focus"""
    global commands_out_of_focus
    if commands_out_of_focus:
        print(f"[CS2 ChatBot] Executing {len(commands_out_of_focus)} out-of-focus commands...")
        for command in commands_out_of_focus:
            execute_command(command)
        commands_out_of_focus.clear()

async def main_loop():
    """Main async loop for processing"""
    global last_line
    
    print(f"[CS2 ChatBot] Monitoring console.log: {globals.LOG_FILE}")
    print(f"[CS2 ChatBot] Available commands: {', '.join([cmd.replace(globals.COMMAND_PREFIX, '') for cmd in COMMANDS.keys()])}")
    
    while True:
        if pyautogui.getActiveWindowTitle() != "Counter-Strike 2":
            if show_debug:
                print("[Debug] CS2 is not focused, cant handle out-of-focus commands...")
            await asyncio.sleep(1)
        else:
            handle_out_of_focus_commands()

        try:
            line = tail_log()
            if line and line != last_line:
                last_line = line
                if show_debug:
                    print(f"[Debug] New line: {line}")  # Debug output
                
                # Parse the chat line
                chat_data = parse_chat_line(line)
                if chat_data:
                    if show_debug:
                        print(f"[Debug] Parsed: {chat_data}")  # Debug output
                    if is_valid_command(chat_data['command']):
                        if show_debug:
                            print(f"[Debug] Valid command detected: {chat_data['command']}")  # Debug output
                        process_command(chat_data)
            
        except KeyboardInterrupt:
            print("\n[CS2 ChatBot] Shutting down...")
            break
        except Exception as e:
            print(f"[Error] {e}")
            await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\n[CS2 ChatBot] Goodbye!")
    except Exception as e:
        print(f"[Fatal Error] {e}")
