from core.database.bank import BankManager
from core.wrapper import Wrapper

from nextcord.ext import commands
from nextcord import SlashOption, Interaction

from os import environ, path
import json

bot = commands.Bot()

@bot.slash_command(name="link", description="Link your ingame account with a token", force_global=True)
@commands.cooldown(1, 120, commands.BucketType.user)
async def link(
    interaction: Interaction,
    token: str = SlashOption(
        name        = "token",
        description = "token to link your account with",
        required    = True
    )
):
    core  = path.dirname(path.abspath(__file__))
    tokens_db = path.join(core, "database", "data", "tokens.json")
    linked_db = path.join(core, "database", "data", "linked.json")

    with open(tokens_db, "r") as f:
        try: tokens = json.load(f)
        except json.JSONDecodeError: tokens = {}

    with open(linked_db, "r") as f:
        try: linked = json.load(f)
        except json.JSONDecodeError: linked = {}

    for player, saved_token in tokens.items():
        if saved_token == token: break

    else:
        return await interaction.response.send_message(
            "❌ **Invalid token**",
            ephemeral=True
        )
    
    del tokens[player]
    with open(tokens_db, "w") as f:
        json.dump(tokens, f, indent=4)
    
    linked[str(interaction.user.id)] = player # type: ignore
    with open(linked_db, "w") as f:
        json.dump(linked, f, indent=4)

    BankManager().deposit(player, 50000000)
    Wrapper().commands.privatemessage(player, "You got ^5$5,000,000 ^7($5m) reward for linking your account")
    print(f"[Bot] {player} linked theyre account")

    return await interaction.response.send_message(
        f"✅ **Successfully linked your account**",
        ephemeral=True
    )

@bot.slash_command(name="unban", description="Unban a player if they are linked (costs 500m)", force_global=True)
async def unban(
    interaction: Interaction,
    player: str = SlashOption(
        name        = "player",
        description = "players name or discord id of the player to unban",
        required    = True
    )
):
    core  = path.dirname(path.abspath(__file__))
    linked_db = path.join(core, "database", "data", "linked.json")

    with open(linked_db, "r") as f:
        try: linked = json.load(f)
        except json.JSONDecodeError: linked = {}

    if player.isdigit():
        name = linked.get(player)
        if not name: 
            return await interaction.response.send_message(
                "❌ **This Discord user is not linked to any account**",
                ephemeral=True
            )
    
    else:
        if player not in linked.values():
            return await interaction.response.send_message(
                "❌ **This player is not linked or does not exist**",
                ephemeral=True
            )
    
    if not player.startswith("@"):
        player = Wrapper().player.player_client_id_from_name(player)

    Wrapper().commands.unban(f"@{player}", f"You got unbanned by {interaction.user.name}") # type: ignore

    return await interaction.response.send_message(
        f"✅ **Successfully unbanned {player}**",
        ephemeral=True
    )

def run_bot() -> None:
    print("[Bot] Starting Bot")
    bot.run(environ["BOT_TOKEN"])