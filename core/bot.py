from nextcord.ext import commands
from nextcord import Activity, ActivityType
import os

from core.wrapper import Wrapper

bot = commands.Bot()

@bot.event
async def on_ready() -> None:
    await bot.change_presence(
        activity=Activity(type=ActivityType.playing, name=f"Watching {len(Wrapper().server.get_players())} gamblers in BrowniesSND")
    )
    
    print(f"[Bot] Logged in as {bot.user}")
    print(f"[Bot] Connected to {bot.guilds} guild")

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Try again later lil man, it broke")

def load_cogs() -> None:
    for file in os.listdir("core/cogs"):
        if not file.startswith("__"):
            cog = f"core.cogs.{file[:-3]}"
            bot.load_extension(cog)
            print(f"[Bot] loaded core.cogs.{file[:-3]}")

def run_bot() -> None:
    print("[Bot] Starting Bot")
    load_cogs
    bot.run(os.environ["BOT_TOKEN"])
