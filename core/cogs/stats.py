import nextcord
from nextcord.ext import commands
from nextcord import SlashOption, Interaction

from core.database.tokens import TokenManager
from core.database.links import LinkManager
from core.database.bank import BankManager
from core.database.stats import StatsManager
from core.wrapper import Wrapper

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
            return await interaction.response.send_message(
                "### Your Stats:\n"
                f"**Wins: {stats["wins"]}**\n"
                f"**Losses: {stats["losses"]}**\n"
                f"**Net: ${stats["net"]}**",
                ephemeral=True
            )
        
        target = None
        if player.startswith("<@") and player.endswith(">"):
            try:
                player_id = int(player.strip("<@!>"))
                target = LinkManager().get_player_by_discord(player_id)  # type: ignore
            except ValueError:
                pass

        if not target:
            player_clean = player.strip().lower()
            target = Wrapper().player.find_player_by_partial_name(player_clean)

        if not target:
            return await interaction.response.send_message(
                f"❌ Could not find player matching {player}",
                ephemeral=True
            )

        StatsManager().ensure(target)
        stats = StatsManager().stats[target]
        return await interaction.response.send_message(
            f"### {player}'s Stats\n"
            f"**Wins: {stats['wins']}**\n"
            f"**Losses: {stats['losses']}**\n"
            f"**Net: ${stats['net']}**",
            ephemeral=True
        )
    
def setup(bot: commands.Bot):
    bot.add_cog(StatsCog(bot))