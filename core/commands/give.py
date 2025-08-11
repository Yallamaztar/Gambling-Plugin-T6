from core.database.bank import BankManager
from core.commands import owners_only, run_command_threaded
from core.utils import parse_amount
from core.wrapper import Wrapper

from typing import Union

class GiveCommand:
    def __init__(self, player: str, target: str, amount: str) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.give(player, target, amount)
    
    @owners_only()
    def give(self, player: str, target: str, _amount: str) -> None:
        target = self.player.find_player_by_partial_name(target)
        if not target:
            self.commands.privatemessage(player, f"Player {target} not found"); return
        
        amount: int = parse_amount(_amount)
        if amount <= 0:
            self.commands.privatemessage(player, "Amount must be positive"); return

        self.bank.deposit(target, amount)
        self.commands.privatemessage(player, f"Gave {target} ${amount}")
        self.commands.privatemessage(target, f"You have gotten ^2${amount} ^7from {player}")

class GiveAllCommand:
    def __init__(self, player: str, amount: str) -> None:
        self.server   = Wrapper().server
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.give_all(player, amount)

    @owners_only()
    def give_all(self, player: str, _amount: str) -> None:
        amount: int = parse_amount(_amount)
        if amount <= 0:
            self.commands.privatemessage(player, "Amount must be positive"); return
        
        for p in self.server.get_players():
            self.bank.deposit(p['name'], amount)
            self.commands.privatemessage(player, f"Gave {p['name']} ${amount}")
            self.commands.privatemessage(p['name'], f"You've gotten ^2${amount} ^7from {player}")
        
        self.commands.say(f"^7Gave ^3{len(self.server.get_players())} ^7players {amount}")

def give(player: str, target: str, amount: str) -> None:
    run_command_threaded(GiveCommand, player, target, amount)

def give_all(player: str, amount: str) -> None:
    run_command_threaded(GiveAllCommand, player, amount)