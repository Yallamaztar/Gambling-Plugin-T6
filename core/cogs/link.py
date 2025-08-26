import nextcord
from nextcord.ext import commands
from nextcord import SlashOption, Interaction

from core.database.tokens import TokenManager
from core.database.links import LinkManager
from core.database.bank import BankManager
from core.wrapper import Wrapper
from core.webhook import link_webhook

class LinkCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(1, 120, commands.BucketType.user)
    @nextcord.slash_command(
        name="link",
        description="Link your ingame account with a token",
        force_global=True
    )
    async def link(
        self,
        interaction: Interaction,
        token: str = SlashOption(
            name="token",
            description="Token to link your account with",
            required=True
        )
    ):  
        player = TokenManager().get_player_by_token(token)
        if not player:
            return await interaction.response.send_message(
                "❌ **Invalid token**", ephemeral=True
            )

        TokenManager().delete(player)
        LinkManager().link_account(interaction.user.id, player)  # type: ignore
        BankManager().deposit(player, 50_000_000)
        Wrapper().commands.privatemessage(player, "You got $50M reward for linking your account")

        link_webhook(player, str(interaction.user.id)) # type: ignore
        print(f"[Bot] {player} linked their account")

        await interaction.response.send_message(
            "✅ **Successfully linked your account ($50M reward)**",
            ephemeral=True
        )

def setup(bot: commands.Bot):
    bot.add_cog(LinkCog(bot))
