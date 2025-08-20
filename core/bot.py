from nextcord.ext import commands
from os import environ

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

cogs = [
    "core.cogs.link",
    "core.cogs.unban",
    "core.cogs.gamble",
    "core.cogs.balance"
    "core.cogs.stats"
]

for cog in cogs:
    bot.load_extension(cog)
    print(f"[Bot] loaded {cog}")

print(f"[Bot] Loaded {len(cogs)} cogs")

def run_bot() -> None:
    print("[Bot] Starting Bot")
    bot.run(environ["BOT_TOKEN"])