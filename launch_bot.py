import os
import globals

def main():
    print("CS2Bot Launcher")
    print("="*50)
    
    # Check if cs2bot.py exists
    if not os.path.exists("cs2bot.py"):
        print("❌ cs2bot.py not found in current directory")
        return
    
    print("✅ cs2bot.py found")
    
    # Try to import the bot
    try:
        import cs2bot
        print("✅ cs2bot imported successfully")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return
    
    # Check if log file path exists
    if os.path.exists(globals.LOG_FILE):
        print(f"✅ Console log file found: {globals.LOG_FILE}")
    else:
        print(f"⚠️  Console log file not found: {globals.LOG_FILE}")
        print("   This is normal if CS2 isn't running or path needs updating")
    
    # Check cfg directory
    cfg_dir = os.path.dirname(globals.CFG_FILE)
    if os.path.exists(cfg_dir):
        print(f"✅ Config directory found: {cfg_dir}")
    else:
        print(f"❌ Config directory not found: {cfg_dir}")
        print("   Please update the CFG_FILE path in cs2bot.py")
        return
    
    print("\n" + "="*50)
    print("Ready to start CS2Bot!")
    print("Available commands:")
    for cmd in cs2bot.COMMANDS.keys():
        # Remove the prefix for display
        display_cmd = cmd.replace(globals.COMMAND_PREFIX, "")
        desc = cs2bot.COMMANDS[cmd]['description']
        print(f"  {display_cmd}: {desc}")
    
    print("\nTo start the bot, run: python cs2bot.py")
    print("Make sure CS2 is running and autoexec.cfg is loaded")
    
    # Ask user if they want to start the bot
    response = input("\nStart bot now? (y/N): ").lower().strip()
    if response == 'y':
        print("\nStarting CS2Bot...")
        try:
            import asyncio
            asyncio.run(cs2bot.main_loop())
        except KeyboardInterrupt:
            print("\n✅ Bot stopped by user")
        except Exception as e:
            print(f"❌ Bot error: {e}")

if __name__ == "__main__":
    main()
