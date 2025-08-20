import nextcord
from nextcord.ext import commands
from nextcord import SlashOption, Interaction

from core.database.links import LinkManager
from core.database.bank import BankManager
from core.wrapper import Wrapper

from typing import Optional

class BalanceCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        name="balance",
        description="Check your own or another players balance",
        force_global=True
    )
    async def balance(
        self,
        interaction: Interaction,
        player: Optional[str] = SlashOption(
            name="player",
            description="view the balance of another player",
            required=False,
        )
    ):
        client = LinkManager().get_player_by_discord(interaction.user.id) # type: ignore
        if not client:
            return await interaction.response.send_message(
                "❌ **You must link your account first to check balance**",
                ephemeral=True
            )

        if not player:
            bal = BankManager().balance(client)
            return await interaction.response.send_message(
                f"Your balance is **${bal}**",
                ephemeral=True
            )

        if isinstance(player, nextcord.Member):
            client = LinkManager().get_player_by_discord(player.id)  # type: ignore
            if not client:
                return await interaction.response.send_message(
                    f"❌ {player.mention} has not linked their account",
                    ephemeral=True
                )
        
            bal = BankManager().balance(client)
            return await interaction.response.send_message(
                f"{player.display_name}s balance is **${bal}**",
                ephemeral=True
            )
        else:
            target = Wrapper().player.find_player_by_partial_name(player)
            if not target:
                return await interaction.response.send_message(
                    f"❌ Could not find player matching {player}",
                    ephemeral=True
                )
        
            bal = BankManager().balance(target)
            return await interaction.response.send_message(
                f"{target}s balance is **${bal}**",
                ephemeral=True
            )
    

def setup(bot: commands.Bot):
    bot.add_cog(BalanceCog(bot))