from core.database.bank import BankManager
from core.database.tokens import TokenManager
from core.database.links import LinkManager
from core.wrapper import Wrapper

from nextcord.ext import commands
from nextcord import SlashOption, Interaction

from os import environ

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

    player = TokenManager().get_player_by_token(token)
    if not player:
        return await interaction.response.send_message(
            "❌ **Invalid token**",
            ephemeral=True
        )
    
    TokenManager().delete(player)
    LinkManager().link_account(interaction.user.id, player) # type: ignore

    BankManager().deposit(player, 50_000_000)
    Wrapper().commands.privatemessage(player, "You got ^5$50,000,000 ^7($50m) reward for linking your account")
    print(f"[Bot] {player} linked their account")

    await interaction.response.send_message(
        "✅ **Successfully linked your account ($50m reward)**",
        ephemeral=True
    )

@bot.slash_command(name="unban", description="Unban a player if they are linked (costs $500m)", force_global=True)
async def unban(
    interaction: Interaction,
    player: str = SlashOption(
        name        = "player",
        description = "Players name or Discord ID to unban",
        required    = True
    )
):     
    price = 500_000_000
    
    executor = LinkManager().get_player_by_discord(interaction.user.id) # type: ignore
    if not executor:
        return await interaction.response.send_message(
            "❌ **You must link your account first to use this command**",
            ephemeral=True
        )
    
    balance = BankManager().balance(executor)
    if balance == 0:
        return await interaction.response.send_message("🏳️‍🌈 **You are gay and poor**")

    if balance < price:
        return await interaction.response.send_message(
            "❌ **You don't have enough money to pay the unban cost ($500M)**",
            ephemeral=True
        )

    if player.isdigit():
        discord_id = LinkManager().get_player_by_discord(int(player))
        if not discord_id:
            return await interaction.response.send_message(
                "❌ **You must link your account first to use this command**",
                ephemeral=True
            )
        player = discord_id
    else:
        if not LinkManager().is_linked(player):
            return await interaction.response.send_message(
                "❌ **This player is not linked or does not exist**",
                ephemeral=True
            )
        
    player_id = Wrapper().player.player_client_id_from_name(player)
    ban_reason = Wrapper().player.ban_reason(player_id)
    if not ban_reason.startswith("You lost gamble lol"): 
        return await interaction.response.send_message(
            "❌ **This player wasn't banned for losing a gamble**",
            ephemeral=True
        )

    unban_target = player_id if player_id.startswith("@") else f"@{player_id}"
    try:
        Wrapper.commands.unban(unban_target, f"You got unbanned by {interaction.user.name}")  # type: ignore
    except Exception:
        return await interaction.response.send_message(
            "❌ **Failed to unban this player. Please try again later.**",
            ephemeral=True
        )
    await interaction.response.send_message(
        f"✅ **Successfully unbanned {player}**",
        ephemeral=True
    )

def run_bot() -> None:
    print("[Bot] Starting Bot")
    bot.run(environ["BOT_TOKEN"])