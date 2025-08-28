from core.database.bank import BankManager
from core.database.links import LinkManager
from core.permissions import PermissionManager, owners_only, admins_only
from core.commands import run_command_threaded, rate_limit
from core.utils import parse_amount, parse_prefix_amount
from core.wrapper import Wrapper

class GiveCommand:
    def __init__(self, player: str, target: str, amount: str) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.give(player, target, amount)
    
    @owners_only()
    def give(self, player: str, target: str, _amount: str) -> None:
        target = LinkManager().find_linked_by_partial_name(target)
        if not target:
            self.commands.privatemessage(player, f"Player {target} not found"); return
        
        amount: int = parse_amount(_amount)
        if amount <= 0:
            self.commands.privatemessage(player, "Amount must be positive"); return

        self.bank.deposit(target, amount)
        self.commands.privatemessage(player, f"Gave {target} ^5${parse_prefix_amount(amount)}^7")
        self.commands.privatemessage(target, f"You have gotten ^2^5${parse_prefix_amount(amount)}^7 ^7from {player}")

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
            self.commands.privatemessage(player, f"Gave {p['name']} ^5${parse_prefix_amount(amount)}^7")
            self.commands.privatemessage(p['name'], f"You've gotten ^2^5${parse_prefix_amount(amount)}^7 ^7from {player}")
        
        self.commands.say(f"^7Gave ^3{len(self.server.get_players())} ^7players ^5${parse_prefix_amount(amount)}^7")

class GiveAdminCommand:
    def __init__(self, player: str, target: str, amount: str) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.MAX_ADMIN_GIVE     = 250_000_000_000 # 250b
        self.give(player, target, amount)

    @admins_only()
    def give(self, player: str, target: str, _amount: str) -> None:
        target = LinkManager().find_linked_by_partial_name(target)
        if not target:
            self.commands.privatemessage(player, f"Player {target} not found"); return
        
        amount: int = parse_amount(_amount)
        if amount <= 0:
            self.commands.privatemessage(player, "Amount must be positive"); return
        
        if amount > self.MAX_ADMIN_GIVE and not PermissionManager().is_owner(player):
            self.commands.privatemessage(player, f"Admins can only give up to ${self.MAX_ADMIN_GIVE}"); return
        
        self.bank.deposit(target, amount)
        self.commands.privatemessage(player, f"Gave {target} ^5${parse_prefix_amount(amount)}^7")
        self.commands.privatemessage(target, f"You have gotten ^5${parse_prefix_amount(amount)}^7")
        print(f"[GiveAdmin] {player} gave {target} ^5${parse_prefix_amount(amount)}^7")

class GiveAllAdminCommand:
    def __init__(self, player: str, amount: str) -> None:
        self.server   = Wrapper().server
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.MAX_ADMIN_GIVE_ALL = 100_000_000_000 # 100b
        
        self.give_all(player, amount)

    @admins_only()
    def give_all(self, player: str, _amount: str) -> None:
        amount: int = parse_amount(_amount)
        if amount <= 0:
            self.commands.privatemessage(player, "Amount must be positive"); return
        
        if amount > self.MAX_ADMIN_GIVE_ALL and not PermissionManager().is_owner(player):
            self.commands.privatemessage(player, f"Admins can only give up to ${self.MAX_ADMIN_GIVE_ALL}"); return

        for p in self.server.get_players():
            self.bank.deposit(p['name'], amount)
            self.commands.privatemessage(player, f"Gave {p['name']} ^5${parse_prefix_amount(amount)}^7")
            self.commands.privatemessage(p['name'], f"You've gotten ^2^5${parse_prefix_amount(amount)}^7 ^7from {player}")
        
        self.commands.say(f"^7Gave ^3{len(self.server.get_players())} ^7players ^5${parse_prefix_amount(amount)}^7")
        print(f"[GiveAllAdmin] {player} gave {len(self.server.get_players())} players ^5${parse_prefix_amount(amount)}^7")
    

def give(player: str, target: str, amount: str) -> None:
    run_command_threaded(GiveCommand, player, target, amount)

def give_all(player: str, amount: str) -> None:
    run_command_threaded(GiveAllCommand, player, amount)

@rate_limit(minutes=30)
def admin_give(player: str, target: str, amount: str) -> None:
    run_command_threaded(GiveAdminCommand, player, target, amount)

@rate_limit(minutes=30)
def admin_give_all(player: str, amount: str) -> None:
    run_command_threaded(GiveAllAdminCommand, player, amount)