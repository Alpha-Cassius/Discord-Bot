import discord
from discord.ext import commands
import customtkinter as ctk
import threading

# Bot Configuration
TOKEN = "YOUR_TOKEN" # Give your token here
intents = discord.Intents.default()
intents.message_content = True  # intent for reading messages
intents.guilds = True
intents.members = True  # intent for member-related commands
bot = commands.Bot(command_prefix="!", intents=intents)

# GUI Setup
class BotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Discord Bot Status")
        self.geometry("400x300")
        self.resizable(0,0)

        self.label = ctk.CTkLabel(self, text="Bot Status: Offline", font=("Arial", 16))
        self.label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Start Bot", command=self.start_bot)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop Bot", command=self.stop_bot, state="disabled")
        self.stop_button.pack(pady=10)

        self.credit_label = ctk.CTkLabel(self, text="Created by Alpha Cassius", font=("Arial", 10))
        self.credit_label.pack(side="bottom", pady=5)
    
    def start_bot(self):
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.label.configure(text="Bot Status: Running")
        threading.Thread(target=run_bot, daemon=True).start()
    
    def stop_bot(self):
        self.label.configure(text="Bot Status: Stopped")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        bot.close()

# Discord Bot Events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I'm your bot!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def kick(ctx, member: discord.Member = None, *, reason="No reason provided"):
    if member is None:
        await ctx.send("⚠️ Please mention a user to kick. Usage: `!kick @username [reason]`")
        return
    
    if ctx.author.guild_permissions.kick_members:
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member.name} has been kicked. Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("I do not have permission to kick members.")
    else:
        await ctx.send("You do not have permission to use this command.")

@bot.command()
async def ban(ctx, member: discord.Member = None, *, reason="No reason provided"):
    if member is None:
        await ctx.send("⚠️ Please mention a user to ban. Usage: `!ban @username [reason]`")
        return
    
    if ctx.author.guild_permissions.ban_members:
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.name} has been banned. Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("I do not have permission to ban members.")
    else:
        await ctx.send("You do not have permission to use this command.")

@bot.command()
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            try:
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name} has been unbanned.")
                return
            except discord.Forbidden:
                await ctx.send("I do not have permission to unban members.")
    await ctx.send(f"User {member_name} not found in ban list.")

def run_bot():
    bot.run(TOKEN)

if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()
