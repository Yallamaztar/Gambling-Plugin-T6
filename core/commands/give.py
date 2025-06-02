from core.database.bank import BankManager
from core.commands import owners_only, run_command_threaded
from core.utils import parse_amount
from core.wrapper import Wrapper

class GiveCommand:
    def __init__(self, player: str, target: str, amount: str) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.give(player, target, amount)
        
    @owners_only()
    def give(self, player: str, target: str, amount: str) -> None:
        target = self.player.find_player_by_partial_name(target)
        self.bank.deposit(target, parse_amount(amount))
        self.commands.privatemessage(player, f"Gave {target} ${amount}")
        self.commands.privatemessage(target, f"You've gotten ^2${amount} ^7from {player}")

class GiveAllCommand:
    def __init__(self, player: str, amount: str) -> None:
        self.server   = Wrapper().server
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.give_all(player, amount)

    @owners_only()
    def give_all(self, player: str, amount: str) -> None:
        for p in self.server.get_players():
            self.bank.deposit(p['name'], parse_amount(amount))
            self.commands.privatemessage(player, f"Gave {p['name']} ${amount}")
            self.commands.privatemessage(p['name'], f"You've gotten ^2${amount} ^7from {player}")

def give(player: str, target: str, amount: str) -> None:
    run_command_threaded(GiveCommand, player, target, amount)

def give_all(player: str, amount: str) -> None:
    run_command_threaded(GiveAllCommand, player, amount)