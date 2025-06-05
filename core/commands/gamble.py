from core.database.bank import BankManager
from core.utils import parse_amount, split_clan_tag, safe_int
from core.wrapper import Wrapper
from core.commands import run_command_threaded
import random

class GambleCommand:
    def __init__(self, player: str, amount: str) -> None:
        self.commands = Wrapper().commands
        self.bank = BankManager()

        try:
            bet = self.validate(player, amount)
            if bet == None: 
                return
            
            result = self.update_balance(player, bet)
            self.commands.privatemessage(player, f"you {result} | Your new balance: ^5${self.bank.balance(player)}")
            if result.startswith("^2"):
                self.commands.say(f"^7{split_clan_tag(player)} {result} ${safe_int(bet)}")
            return
        
        except ValueError:
            return self.commands.privatemessage(player, f"{amount} ^1is not^7 a valid number")

    def validate(self, player: str, amount: str) -> int:
        if amount.lower() == "all":
            bet = self.bank.balance(player)
            if bet <= 0:
                self.commands.say(f"^7@{player} is ^1^Fgay n poor")
                return 
            return bet
        
        else:
            bet = parse_amount(amount)
            bal = self.bank.balance(player)
            
            if bet <= 0:
                return self.commands.privatemessage(player, f"^1cannot pay^7 non-positive amount: {amount}")
            if bal < bet:
                return self.commands.privatemessage(player, f"^1cannot^7 bet ${bet}, you ^3only^7 have ^1${bal}")
        
        return bet
                
    def update_balance(self, player: str, bet: int) -> str:
        bet = safe_int(bet)
        if random.choice([True, False]):
            self.bank.deposit(player, bet)
            result = "^2won^7"
        else:
            self.bank.deposit(player, -bet)
            result = "^1lost^7"

        return result
    
def gamble(player: str, amount: str) -> None:
    run_command_threaded(GambleCommand, player, amount)