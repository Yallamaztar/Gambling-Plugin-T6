import nextcord
from nextcord.ext import commands
from nextcord import SlashOption, Interaction

from core.database.links import LinkManager
from core.database.bank import BankManager
from core.database.stats import StatsManager
from core.wrapper import Wrapper
from core.utils import parse_prefix_amount

from typing import Optional

class StatsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        name="pay",
        description="Pay a player money (only linked players)",
        force_global=True
    )
    async def stats(
        self,
        interaction: Interaction,
        player: str = SlashOption(
            name="player",
            description="Pay a player",
            required=True,
        ),
        amount: int = SlashOption(
            name="amount",
            description="Amount to pay",
            required=True
        )
    ):  
        await interaction.response.defer(ephemeral=True)

        client = LinkManager().get_player_by_discord(interaction.user.id)  # type: ignore
        if not client:
            return await interaction.followup.send(
                "❌ **You must link your account first to check stats**",
                ephemeral=True
            )
        
        if amount <= 0:
            return await interaction.followup.send(
                f"❌ **{amount} is an invalid number**",
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
                
        BankManager().deposit(target, amount)
        return await interaction.followup.send(
            f"✅ **{target}** has been unbanned (cost: ${parse_prefix_amount(amount)})",
            ephemeral=True
        )