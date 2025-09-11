import nextcord
from nextcord.ext import commands
from nextcord import SlashOption, Interaction

from core.database.links import LinkManager
from core.database.bank import BankManager
from core.utils import parse_prefix_amount, parse_amount

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
        await interaction.response.defer(ephemeral=True)

        client = LinkManager().get_player_by_discord(interaction.user.id)  # type: ignore
        if not client:
            return await interaction.followup.send(
                "❌ **You must link your account first to check balance**",
                ephemeral=True
            )

        if not player:
            bal = BankManager().balance(client)
            return await interaction.followup.send(
                f"Your balance is {bal} (${parse_prefix_amount(bal)})",
                ephemeral=True
            )
        
        links = LinkManager().load()
        if player in links: target = links[player]
        elif player in links.values(): target = player
        else:
            target = LinkManager().find_linked_by_partial_name(player)
            if not target:
                return await interaction.followup.send(
                    f"❌ Could not find a linked account for {player}",
                    ephemeral=True
                )
        
        bal = BankManager().balance(target)
        return await interaction.followup.send(
            f"{target}'s balance is {bal} (${parse_prefix_amount(bal)})",
            ephemeral=True
        )
    
def setup(bot: commands.Bot):
    bot.add_cog(BalanceCog(bot))
