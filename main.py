import discord
from discord.ext import commands
import customtkinter as ctk
import threading
import asyncio

from AI_FEATURES.IMAGE import generate_image
from AI_FEATURES.TEXT import chatting

# Bot Configuration
TOKEN = "YOUR_TOKEN"  # Replace with your actual bot token
intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True
intents.members = True  
bot = commands.Bot(command_prefix="!", intents=intents)

# Global variables
bot_task = None
loop = None

# GUI Setup
class BotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Discord Bot Control")
        self.geometry("400x300")
        self.resizable(0, 0)

        self.label = ctk.CTkLabel(self, text="Bot Status: Offline", font=("Arial", 16))
        self.label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Start Bot", command=self.start_bot)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop Bot", command=self.stop_bot, state="disabled")
        self.stop_button.pack(pady=10)

        self.credit_label = ctk.CTkLabel(self, text="Created by Alpha Cassius", font=("Arial", 10))
        self.credit_label.pack(side="bottom", pady=5)

        self.check_bot_status()

    def check_bot_status(self):
        """Continuously checks if the bot is running and updates button states."""
        global bot_task, bot_running
        if bot_task and bot_task.is_alive():
            bot_running = True
            self.label.configure(text="Bot Status: Running")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
        else:
            bot_running = False
            self.label.configure(text="Bot Status: Offline")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

        # Re-run this method every second
        self.after(1000, self.check_bot_status)

    def start_bot(self):
        global bot_task, loop, bot_running
        if bot_running:  # Prevent multiple instances
            return  

        self.label.configure(text="Bot Status: Starting...")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        bot_running = True
        loop = asyncio.new_event_loop()
        bot_task = threading.Thread(target=run_bot, args=(loop,), daemon=True)
        bot_task.start()

    def stop_bot(self):
        global bot_running, loop
        if bot_running:
            self.label.configure(text="Bot Status: Stopping...")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

            bot_running = False

            if loop:
                loop.call_soon_threadsafe(asyncio.create_task, stop_bot_async())

async def stop_bot_async():
    """Stops the bot safely without crashing."""
    await bot.close()

def run_bot(loop):
    """Runs the bot in an asyncio event loop."""
    global bot_running
    asyncio.set_event_loop(loop)
    bot_running = True
    loop.run_until_complete(bot.start(TOKEN))
    bot_running = False  # Reset when bot stops

# Discord Bot Events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

# New Feature: Handling Messages for Image Generation & AI Chat Response
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself
    
    if message.content and len(message.content) <= 500:
        if "generate" in message.content.lower():
            await message.channel.send(f"Please wait {message.author}...")
            image_details = generate_image(message.content.lower())

            if image_details[1] == 0:
                await message.channel.send(f"{image_details[0]}")  # Error message
            else:
                await message.channel.send(f"{message.author.mention}", file=discord.File(image_details[0]))
        else:
            response = chatting(message.content)
            await message.channel.send(f"{response}")

    await bot.process_commands(message)  # Ensure commands still work

if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()
