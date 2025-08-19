from core.database.bank import BankManager
from core.utils import parse_amount, split_clan_tag
from core.wrapper import Wrapper
from core.commands import run_command_threaded

from typing import Optional, Tuple
import random 


class BanFlip:
    def __init__(self, player: str, amount: str, duration: str) -> None:
        self.commands = Wrapper().commands
        self.bank = BankManager()

        try:
            bet = self.validate(player, amount)
            if bet == None or bet <= 0: return

            multiplier = self.calc_multiplier(player, duration)
            if multiplier is None: return

            result, total = self.update_balance(player, bet, multiplier)
            self.commands.privatemessage(player, f"you {result} | Your new balance: ^5${self.bank.balance(player)}")
            self.commands.say(f"^7{split_clan_tag(player)} {result} ${total}")

            if result == "^1lost^7":
                self.commands.tempban(player, duration, "You lost gamble lol")

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
    
    def calc_multiplier(self, player: str, duration: str) -> Optional[int]:
        unit = duration[-1].lower()
        dur  = int(duration[:-1])

        if unit not in ["m", "h", "d"]:
            self.commands.privatemessage(player, "Invalid time unit, use m, h, or d"); return

        if dur <= 5:
            self.commands.privatemessage(player, "Duration has to be greater than 5"); return
        
        if unit == "m" and dur > 60:
            self.commands.privatemessage(player, "Minutes cannot exceed 60"); return
        if unit == "h" and dur > 24:
            self.commands.privatemessage(player, "Hours cannot exceed 24"); return
        if unit == "d" and dur > 30:
            self.commands.privatemessage(player, "Days cannot exceed 30"); return

        if unit == "m":
            if dur < 5: return 1
            elif dur < 10: return 2
            elif dur < 20: return 3
            elif dur < 30: return 4
            elif dur < 45: return 5
            else: return 6
    
        elif unit == "h":
            if dur < 2: return 4
            elif dur < 3: return 5
            elif dur < 4: return 6
            elif dur < 6: return 7
            elif dur < 8: return 9
            else: return 10

        elif unit == "d":
            if dur < 2: return 10
            elif dur <= 3: return 12
            elif dur <= 5: return 15
            elif dur <= 7: return 17
            elif dur <= 10: return 20
            elif dur <= 15: return 22
            elif dur <= 20: return 25
            elif dur <= 25: return 30
            else: return 45


    def update_balance(self, player: str, bet: int, multiplier: int) -> Tuple[str, Optional[int]]:
        if random.choice([True, False]):
            total = bet * multiplier
            self.bank.deposit(player, total); return ("^2won^7", total)
        else:
            self.bank.deposit(player, -bet); return ("^1lost^7", bet)

def banflip(player: str, amount: str, duration: str) -> None:
    run_command_threaded(BanFlip, player, amount, duration)
