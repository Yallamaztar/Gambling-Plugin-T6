import nextcord
from nextcord.ext import commands

from os import environ

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.http.bulk_upsert_global_commands(bot.user.id, []) # type: ignore
    print("Cleared all global commands!")

cogs = ["cogs.link", "cogs.unban", "cogs.gamble"]
for cog in cogs:
    bot.load_extension(cog)

def run_bot() -> None:
    print("[Bot] Starting Bot")
    bot.run(environ["BOT_TOKEN"])