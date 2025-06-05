from core.wrapper import Wrapper
from core.database.bank import BankManager
from core.commands import run_command_threaded
from typing import Optional

class BalanceCommand:
    def __init__(self, player: str, target: Optional[str] = None) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        if target == None:
            bal = self.bank.balance(player)
            self.commands.privatemessage(player, f"your balance is ^1${bal}")
        else:
            bal = self.bank.balance(self.player.find_player_by_partial_name(target))
            self.commands.privatemessage(player, f"{target}'s balance is ^1${bal}")
        
        return
    
def balance(player: str, target: Optional[str] = None) -> None:
    run_command_threaded(BalanceCommand, player, target)