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
        description="Unban a player if they are linked (costs $10b)",
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
        await interaction.response.defer(ephemeral=True)

        price = 10_000_000_000
        link_manager = LinkManager()
        bank_manager = BankManager()
        wrapper = Wrapper()

        executor = link_manager.get_player_by_discord(interaction.user.id)  # type: ignore
        if not executor:
            return await interaction.followup.send(
                "❌ **You must link your account first**",
                ephemeral=True
            )

        balance = bank_manager.balance(executor)
        if balance < price:
            return await interaction.followup.send(
                f"❌ **You don't have enough money to pay the unban cost (${price:,})**",
                ephemeral=True
            )

        if player.isdigit():
            linked = link_manager.get_player_by_discord(int(player))
            if not linked:
                return await interaction.followup.send(
                    "❌ **That Discord ID is not linked to any player**",
                    ephemeral=True
                )
            player = linked
        elif not link_manager.is_linked(player):
            return await interaction.followup.send(
                "❌ **This player is not linked or does not exist**",
                ephemeral=True
            )

        try:
            player_id = wrapper.player.player_client_id_from_name(player)
        except (IndexError, ValueError, TypeError) as e:
            print(f"[DEBUG] Failed to resolve player_id for {player}: {e}")
            return await interaction.followup.send(
                "❌ **Could not resolve this player in the database**",
                ephemeral=True
            )

        try:
            ban_reason = wrapper.player.ban_reason(player_id)
        except Exception as e:
            print(f"[DEBUG] Failed to fetch ban_reason for {player_id}: {e}")
            return await interaction.followup.send(
                "❌ **Failed to check ban status. Try again later**",
                ephemeral=True
            )

        if not ban_reason or not ban_reason.startswith("You lost gamble lol"):
            return await interaction.followup.send(
                "❌ **This player wasn't banned for losing a gamble**",
                ephemeral=True
            )

        unban_target = f"@{player_id}" if not str(player_id).startswith("@") else str(player_id)

        try:
            wrapper.commands.unban(unban_target, f"You got unbanned by {interaction.user.name}")  # type: ignore
        except Exception as e:
            print(f"[DEBUG] Unban failed for {unban_target}: {e}")
            return await interaction.followup.send(
                "❌ **Failed to unban this player. Try again later**",
                ephemeral=True
            )

        print(f"[Bot] {executor} unbanned {unban_target}")
        unban_webhook(executor, unban_target)

        await interaction.followup.send(
            f"✅ **Successfully unbanned {player}**",
            ephemeral=True
        )


def setup(bot: commands.Bot):
    bot.add_cog(UnbanCog(bot))