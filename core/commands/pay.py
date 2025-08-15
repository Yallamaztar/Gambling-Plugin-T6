from core.database.bank import BankManager
from core.utils import parse_amount
from core.wrapper import Wrapper
from core.commands import run_command_threaded

class PayCommand:
    def __init__(self, player: str, target: str, amount: str) -> None:
        self._player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        target = self._player.find_player_by_partial_name(target)
        if not target:
            self.commands.privatemessage(player, f"Player {target} not found"); return

        try:
            payment = self.validate(player, target, amount)
            if payment == None: return
            
            self.bank.deposit(player, -payment)
            self.bank.deposit(target, payment)

            self.commands.privatemessage(player, f"you have paid ^2${payment}^7 to {target} | Your new balance: ^5${self.bank.balance(player)}")
            self.commands.privatemessage(target, f"{player} paid you ^2${amount}^7 | Your new balance: ^5${self.bank.balance(target)}")
        
        except ValueError:
            return self.commands.privatemessage(player, f"^1{amount}^7 is ^1not^7 a valid number")

    def validate(self, player: str, target: str, amount: str) -> int | None:
        if player == target:
            self.commands.privatemessage(player, "You cannot pay yourself.."); return

        if amount.lower() == "all" or amount.lower() == "a":
            payment = self.bank.balance(player)
            if payment <= 0:
                self.commands.say(f"^7@{player} is ^1^Fgay n poor"); return

        elif amount.lower() == "half" or amount.lower() == "h":
            payment = self.bank.balance(player) // 2
            if payment <= 0:    
                self.commands.say(f"^7@{player} is ^1^Fgay n poor"); return
        
        else:
            payment = parse_amount(amount)
            bal = self.bank.balance(player)

            if payment <= 0:
                self.commands.privatemessage(
                    player, f"^1cannot pay^7 non-positive amount: {amount}"
                ); return
            
            if bal < payment:
                self.commands.privatemessage(
                    player, f"^1cannot^7 pay ${payment}, you ^3only^7 have ^1${bal}"
                ); return
            
        return payment
    
def pay(player: str, target: str, amount: str) -> None:
    run_command_threaded(PayCommand, player, target, amount)