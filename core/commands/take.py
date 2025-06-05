from core.database.bank import BankManager
from core.commands import owners_only, run_command_threaded
from core.utils import parse_amount
from core.wrapper import Wrapper

class TakeCommand:
    def __init__(self, player: str, target: str, amount: str) -> None:
        self.server   = Wrapper().server
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.take(player, target, amount)
        return
    
    @owners_only()
    def take(self, player: str, target: str, amount: str) -> None:
        target = self.player.find_player_by_partial_name(target)
        amount = self.validate(player, target, amount)

        self.bank.deposit(target, -amount)
        self.commands.privatemessage(player, f"Took ^1${amount} ^7from player")
        self.commands.privatemessage(target, f"{player} took ^1${amount} ^7from you")

    def validate(self, player: str, target: str, amount: str) -> int:
        if amount.lower() == "all":
            return self.bank.balance(target)
        else:
            amount = parse_amount(amount)
            bal = self.bank.balance(target)

            if amount > bal:
                return self.commands.privatemessage(player, f"^1cannot^7 take {amount} from {target}")
            
        return amount

class TakeAllCommand:
    def __init__(self, player: str, amount: str) -> None:
        self.server   = Wrapper().server
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.take_all(player, amount)
        return
    
    @owners_only()
    def take_all(self, player: str, amount: str) -> None:
        for p in self.server.get_players():
            bal = self.bank.balance(p['name'])
            if bal == 0: return
            self.bank.deposit(p['name'], -parse_amount(amount))
            
        self.commands.privatemessage(player, f"Took {len(self.server.get_players())} players money")

def take(player: str, target: str, amount: str) -> None:
    run_command_threaded(TakeCommand, player, target, amount)

def take_all(player: str, amount: str) -> None:
    run_command_threaded(TakeAllCommand, player, amount)

    