from core.database.bank import BankManager
from core.utils import parse_amount, split_clan_tag
from core.wrapper import Wrapper
from core.commands import run_command_threaded

from typing import Optional
import random

class GambleCommand:
    def __init__(self, player: str, amount: str) -> None:
        self.commands = Wrapper().commands
        self.bank = BankManager()

        try:
            bet = self.validate(player, amount)
            if bet == None or bet <= 0: return
            
            result = self.update_balance(player, bet)
            self.commands.privatemessage(player, f"you {result} | Your new balance: ^5${self.bank.balance(player)}")
            self.commands.say(f"^7{split_clan_tag(player)} {result} ${bet}")
        
        except ValueError:
            self.commands.privatemessage(player, f"{amount} ^1is not^7 a valid number")

    def validate(self, player: str, amount: str) -> Optional[int]:
        if amount.lower() == "all" or amount.lower() == "a":
            bet = self.bank.balance(player)
            if bet <= 0:
                self.commands.say(f"^7@{player} is ^1^Fgay n poor"); return
            
            return bet
        
        elif amount.lower() == "half" or amount.lower() == "h":
            bet = self.bank.balance(player) // 2
            if bet <= 0:
                self.commands.say(f"^7@{player} is ^1^Fgay n poor"); return
            
            return bet
        
        bet = parse_amount(amount)
        bal = self.bank.balance(player)
            
        if bet <= 0:
            self.commands.say(f"^7@{player} is ^1^Fgay n poor"); return
        
        if bal < bet:
            self.commands.privatemessage(player, f"^1cannot^7 bet ${bet}, you ^3only^7 have ^1${bal}"); return
        
        return bet
                
    def update_balance(self, player: str, bet: int) -> str:
        if random.choice([True, False]):
            self.bank.deposit(player, bet); return "^2won^7"
        else:
            self.bank.deposit(player, -bet); return "^1lost^7"

def gamble(player: str, amount: str) -> None:
    run_command_threaded(GambleCommand, player, amount)