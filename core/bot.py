from nextcord.ext import commands, tasks
from nextcord import Activity, ActivityType
import os, asyncio

from core.wrapper import Wrapper

bot = commands.Bot()

@bot.event
async def on_ready() -> None:
    print(f"[Bot] Logged in as {bot.user}")
    for guild in bot.guilds:
        print(f"[Bot] Connected to {guild.name} - ID: {guild.id}")

    if not update_presence.is_running():
        update_presence.start()

@tasks.loop(seconds=5)
async def update_presence() -> None:
    await bot.change_presence(
        activity=Activity(
            type=ActivityType.playing, 
            name=f"Watching {len(Wrapper().server.get_players())} gamblers on Brownies <3"
        )
    )
@bot.event
async def on_command_error(ctx, error) -> None:
    await ctx.send(f"Try again later lil man, it broke")

def load_cogs() -> None:
    for file in os.listdir("core/cogs"):
        if not file.startswith("__"):
            cog = f"core.cogs.{file[:-3]}"
            bot.load_extension(cog)
            print(f"[Bot] loaded core.cogs.{file[:-3]}")

def run_bot() -> None:
    print("[Bot] Starting Bot")
    load_cogs()
    bot.run(os.environ["BOT_TOKEN"])
