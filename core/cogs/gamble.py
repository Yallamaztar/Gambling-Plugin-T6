import nextcord
from nextcord.ext import commands
from nextcord import SlashOption, Interaction

from core.database.bank import BankManager
from core.database.links import LinkManager
from core.database.stats import StatsManager
from core.wrapper import Wrapper
from core.webhook import win_webhook, loss_webhook
from core.utils import parse_amount, parse_prefix_amount, split_clan_tag

import random
from typing import Optional

class GambleCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bank = BankManager()
        self.commands = Wrapper().commands
        self.links = LinkManager()

    @nextcord.slash_command(
        name="gamble",
        description="Gamble your money with a 50/50 chance",
        force_global=True
    )
    async def gamble(
        self,
        interaction: Interaction,
        amount: str = SlashOption(
            name="amount",
            description="Amount to gamble (number, 'all', 'half')",
            required=True
        )
    ):
        await interaction.response.defer(ephemeral=True)

        player = self.links.get_player_by_discord(interaction.user.id) # type: ignore
        if not player:
            return await interaction.followup.send(
                "❌ **You must link your account first to gamble**",
                ephemeral=True
            )

        bet = self.validate_bet(player, amount)
        if not bet:
            return await interaction.followup.send(
                "❌ Invalid bet amount or insufficient balance",
                ephemeral=True
            )

        result = self.update_balance(player, bet)
        self.commands.say(f"^7{split_clan_tag(player)} {result} ^5${parse_prefix_amount(bet)}^7")

        await interaction.followup.send(
            f"🎲 **You {result} ${parse_prefix_amount(bet)}** Your new balance: ${self.bank.balance(player)}",
            ephemeral=True
        )

    def validate_bet(self, player: str, amount: str) -> Optional[int]:
        bal = self.bank.balance(player)

        if amount.lower() in ("all", "a"):
            if bal <= 0: return None
            return bal
        elif amount.lower() in ("half", "h"):
            if bal <= 0: return None
            return bal // 2

        bet = parse_amount(amount)
        if bet <= 0 or bet > bal:
            return None
        return bet

    def update_balance(self, player: str, bet: int) -> str:
        if random.random() < 0.45:
            win_amount = int(bet * 0.95)
            self.bank.deposit(player, win_amount)
            win_webhook(player, str(win_amount))
            StatsManager().win(player, win_amount)
            return "won"
        else:
            self.bank.deposit(player, -bet)
            loss_webhook(player, str(bet))
            StatsManager().loss(player, bet)
            return "lost"

def setup(bot: commands.Bot):
    bot.add_cog(GambleCog(bot))