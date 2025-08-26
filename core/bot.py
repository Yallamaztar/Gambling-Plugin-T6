from nextcord.ext import commands
import os

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f"[Bot] Logged in as {bot.user}")

for file in os.listdir("core/cogs"):
    if not file.startswith("__"):
        bot.load_extension(f"core.cogs.{file[:-3]}")
        print(f"[Bot] loaded core.cogs.{file[:-3]}")

def run_bot() -> None:
    print("[Bot] Starting Bot")
    bot.run(os.environ["BOT_TOKEN"])