from core.database.bank import BankManager
from core.database.links import LinkManager
from core.commands import run_command_threaded, rate_limit
from core.permissions import admins_only, owners_only
from core.utils import parse_amount, parse_prefix_amount
from core.wrapper import Wrapper

class TakeCommand:
    def __init__(self, player: str, target: str, amount: str) -> None:
        self.server   = Wrapper().server
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.take(player, target, amount)
    
    @admins_only()
    def take(self, player: str, target: str, _amount: str) -> None:
        target = LinkManager().find_linked_by_partial_name(target)
        if not target:
            self.commands.privatemessage(player, f"Player {target} not found"); return
        
        balance = self.bank.balance(target)
        if balance == 0:
            self.commands.privatemessage(player, f"{target} has ^1no ^7money"); return
        
        if _amount.lower() == "all" or _amount.lower() == "a":
            amount = balance

        elif _amount.lower() == "half" or _amount.lower() == "h":
            amount = balance // 2
            if amount <= 0:
                self.commands.privatemessage(player, f"{target} doesnt have enough money to take half"); return
            
        else:
            amount = parse_amount(_amount)
            if amount > balance:
                amount = balance

        self.bank.deposit(target, -amount)
        print(f"[TakeCommand] {player} took ^5${parse_prefix_amount(amount)}^7 from {target}")
        self.commands.privatemessage(player, f"Took ^5${parse_prefix_amount(amount)}^7 ^7from player")
        self.commands.privatemessage(target, f"{player} took ^5${parse_prefix_amount(amount)}^7 ^7from you")

class TakeAllCommand:
    def __init__(self, player: str, amount: str) -> None:
        self.server   = Wrapper().server
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.take_all(player, amount)
    
    @owners_only()
    def take_all(self, player: str, _amount: str) -> None:
        count = 0

        for p in self.server.get_players():
            balance = self.bank.balance(p['name'])
            if balance == 0: continue
            
            if _amount.lower() == "all" or _amount.lower() == "a":
                amount = balance

            elif _amount.lower() == "half" or _amount.lower() == "h":
                amount = balance // 2
                if amount <= 0: continue

            else:
                amount = parse_amount(_amount)
                if amount > balance: amount = balance

            self.bank.deposit(p['name'], -amount)
            self.commands.privatemessage(player, f"Took ^5${parse_prefix_amount(amount)}^7 ^7from {p['name']}")
            self.commands.privatemessage(p['name'], f"{player} took ^1${balance} ^7from you")
            count += 1

        self.commands.privatemessage(player, f"Took {count} players money")


@rate_limit(hours=2)
def take(player: str, target: str, amount: str) -> None:
    run_command_threaded(TakeCommand, player, target, amount)

def take_all(player: str, amount: str) -> None:
    run_command_threaded(TakeAllCommand, player, amount)

    