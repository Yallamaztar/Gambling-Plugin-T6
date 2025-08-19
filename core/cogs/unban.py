import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption

from core.database.links import LinkManager
from core.database.bank import BankManager
from core.wrapper import Wrapper

class UnbanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="unban",
        description="Unban a player if they are linked (costs $500M)",
        force_global=True
    )
    async def unban(
        self,
        interaction: Interaction,
        player: str = SlashOption(
            name="player",
            description="Players name or Discord ID to unban",
            required=True
        )
    ):
        price = 500_000_000
        executor = LinkManager().get_player_by_discord(interaction.user.id)  # type: ignore

        if not executor:
            return await interaction.response.send_message(
                "❌ **You must link your account first**", ephemeral=True
            )

        balance = BankManager().balance(executor)
        if balance < price:
            return await interaction.response.send_message(
                "❌ **You don't have enough money to pay the unban cost ($500M)**",
                ephemeral=True
            )

        if player.isdigit():
            player = LinkManager().get_player_by_discord(int(player)) or player
        elif not LinkManager().is_linked(player):
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

        unban = f"@{player_id}" if not str(player_id).startswith("@") else str(player_id)
        try:
            Wrapper().commands.unban(unban, f"You got unbanned by {interaction.user.name}")  # type: ignore
        except Exception:
            return await interaction.response.send_message(
                "❌ **Failed to unban this player. Try again later**",
                ephemeral=True
            )

        await interaction.response.send_message(
            f"✅ **Successfully unbanned {player}**",
            ephemeral=True
        )

def setup(bot: commands.Bot):
    bot.add_cog(UnbanCog(bot))
