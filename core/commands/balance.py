from core.wrapper import Wrapper
from core.database.bank import BankManager
from core.database.links import LinkManager
from core.commands import run_command_threaded
from core.permissions import discord_linked_only
from typing import Optional

class BalanceCommand:
    def __init__(self, player: str, target: Optional[str] = None) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        if target == None:
            bal = self.bank.balance(player)
            self.commands.privatemessage(player, f"your balance is ^1${bal}"); return
        
        target = LinkManager().find_linked_by_partial_name(target) # type: ignore
        bal = self.bank.balance(target)
        self.commands.privatemessage(player, f"{target}'s balance is ^1${bal}")

@discord_linked_only()
def balance(player: str, target: Optional[str] = None) -> None:
    run_command_threaded(BalanceCommand, player, target)