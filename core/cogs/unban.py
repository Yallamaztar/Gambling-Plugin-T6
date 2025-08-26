import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption

from core.database.links import LinkManager
from core.database.bank import BankManager
from core.wrapper import Wrapper
from core.webhook import unban_webhook


class UnbanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="unban",
        description=r"Unban a player if they are linked (costs 1/3rd of your balance)",
        force_global=True
    )
    async def unban(
        self,
        interaction: Interaction,
        player: str = SlashOption(
            name="player",
            description="Player name (partial), exact name, or Discord ID",
            required=True
        )
    ):
        await interaction.response.defer(ephemeral=True)

        link_manager = LinkManager()
        bank_manager = BankManager()
        wrapper = Wrapper()

        client = link_manager.get_player_by_discord(interaction.user.id)  # type: ignore
        if not client:
            return await interaction.followup.send(
                "❌ **You must link your account first**",
                ephemeral=True
            )

        price = int(0.35 * bank_manager.balance(client))
        if price <= 0: 
            return await interaction.followup.send(
                    f"❌ **You don't have enough money to pay the unban cost (${price:,})**",
                    ephemeral=True
                )
        
        if price <= 500_000_000_000_000: # 500t
            return await interaction.followup.send(
                f"❌ **You don't have enough money to pay the unban cost (${price:,})**",
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
            
        target_id = wrapper.player.player_client_id_from_name(target)
        if not target_id:
            return await interaction.followup.send(
                f"❌ Could not find client ID of {target}",
                ephemeral=True
            )
        
        ban_reason = wrapper.player.ban_reason(target_id)
        if not ban_reason or not ban_reason.startswith("You lost gamble lol"):
            return await interaction.followup.send(
                "❌ **This player wasn't banned for losing a gamble**",
                ephemeral=True
            )
        
        wrapper.commands.unban(f"@{target_id}", f"Gambling unban - {interaction.user.name}")  # type: ignore
        bank_manager.deposit(client, -price)
        unban_webhook(interaction.user.name, target) # type: ignore

        return await interaction.followup.send(
            f"✅ **{target}** has been unbanned (cost: ${price:,})",
            ephemeral=True
        )
    
def setup(bot: commands.Bot):
    bot.add_cog(UnbanCog(bot))
