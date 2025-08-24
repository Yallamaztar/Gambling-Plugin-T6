from nextcord.ext import commands
import os

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f"[Bot] Logged in as {bot.user}")

for file in os.listdir("cogs"):
    if not file.startswith("__"):
        bot.load_extension(file)
        print("[Bot] loaded cog: ", file)

def run_bot() -> None:
    print("[Bot] Starting Bot")
    bot.run(os.environ["BOT_TOKEN"])