import nextcord
from nextcord.ext import commands
from nextcord import SlashOption, Interaction

from core.database.links import LinkManager
from core.database.bank import BankManager
from core.database.stats import StatsManager
from core.utils import parse_prefix_amount

from typing import Optional

class StatsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        name="stats",
        description="Check your own or another players gambling stats",
        force_global=True
    )
    async def stats(
        self,
        interaction: Interaction,
        player: Optional[str] = SlashOption(
            name="player",
            description="view the stats of another player",
            required=False,
        )
    ):
        client = LinkManager().get_player_by_discord(interaction.user.id)  # type: ignore
        if not client:
            return await interaction.response.send_message(
                "❌ **You must link your account first to check stats**",
                ephemeral=True
            )
        
        if not player:
            StatsManager().ensure(client)
            stats = StatsManager().stats[client]
            balance = BankManager().balance(client)

            return await interaction.response.send_message(
                "### Your Stats:\n"
                f"**Wins: {stats["wins"]}**\n"
                f"**Losses: {stats["losses"]}**\n"
                f"**Balance: ${parse_prefix_amount(balance)}**"
                f"**Net: ${stats["net"]}**",
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

        StatsManager().ensure(target)
        stats   = StatsManager().stats[target]
        balance = BankManager().balance(target)
        
        return await interaction.response.send_message(
            f"### {target}'s Stats\n"
            f"**Wins: {stats['wins']}**\n"
            f"**Losses: {stats['losses']}**\n"
            f"**Balance: ${parse_prefix_amount(balance)}**"
            f"**Net: ${stats['net']}**",
            ephemeral=True
        )
    
def setup(bot: commands.Bot):
    bot.add_cog(StatsCog(bot))