import nextcord
from nextcord.ext import commands

from os import environ

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    #await bot.http.bulk_upsert_global_commands(bot.user.id, []) # type: ignore
    #print("Cleared all global commands!")

cogs = [
    "core.cogs.link",
    "core.cogs.unban",
    "core.cogs.gamble"
]

for cog in cogs:
    bot.load_extension(cog)

def run_bot() -> None:
    print("[Bot] Starting Bot")
    bot.run(environ["BOT_TOKEN"])