from core.database.bank import BankManager
from core.database.links import LinkManager
from core.utils import parse_amount, parse_prefix_amount, split_clan_tag
from core.wrapper import Wrapper
from core.commands import run_command_threaded
from core.webhook import banflip_win_webhook, banflip_loss_webhook

from typing import Optional, Tuple
import random 

class BanFlip:
    def __init__(self, player: str, amount: str, duration: str) -> None:
        print(f"[BanFlip] {player} {amount} {duration}")
        
        self.wrapper  = Wrapper()
        self.commands = self.wrapper.commands
        self.links    = LinkManager()

        if not self.links.is_linked(player):
            self.commands.privatemessage(player, "^1You must link your Discord account to use this command. Use ^3!link ^1to link your account.")
            return
        
        self.bank  = BankManager()
        
        try:
            bet = self.validate(player, amount)
            if bet == None or bet <= 0: return

            multiplier = self.calc_multiplier(player, duration)
            if multiplier is None: return

            result, total = self.update_balance(player, bet, multiplier)
            self.commands.privatemessage(player, f"you {result} ${parse_prefix_amount(bet)} | Your new balance: ^5${self.bank.balance(player)}")
            self.commands.say(f"^7{split_clan_tag(player)} {result} ${parse_prefix_amount(bet)}")

            if result == "^1lost^7":
                banflip_loss_webhook(player, str(total), duration)
                self.commands.tempban(player, duration, "You lost gamble lol")
            else:
                banflip_win_webhook(player, str(total), duration)

        except ValueError:
            self.commands.privatemessage(player, f"{amount} ^1is not^7 a valid number")
    
    def validate(self, player: str, amount: str) -> Optional[int]:
        if self.wrapper.player.is_banned(
            self.wrapper.player.player_client_id_from_name(player)
        ):
            self.commands.privatemessage(player, "You cannot run this command"); return

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

        if unit not in ["h", "d"]:
            self.commands.privatemessage(player, "Invalid time unit, use m, h, or d"); return

        if dur < 5 and unit == "m":
            self.commands.privatemessage(player, "Duration has to be greater than 5m"); return
        if unit == "h" and dur > 24:
            self.commands.privatemessage(player, "Hours cannot exceed 24"); return
        if unit == "d" and dur > 30:
            self.commands.privatemessage(player, "Days cannot exceed 30"); return

        elif unit == "h":
            if dur < 12: return 2
            else: return 3

        elif unit == "d":
            if dur < 5: return 4
            if dur < 16: return 5
            else: return 5

    def update_balance(self, player: str, bet: int, multiplier: int) -> Tuple[str, Optional[int]]:
        if random.random() < 0.40:
            total = int(bet * multiplier * 0.90)
            self.bank.deposit(player, total); return ("^2won^7", total)
        else:
            self.bank.deposit(player, -bet); return ("^1lost^7", bet)

def banflip(player: str, amount: str, duration: str) -> None:
    run_command_threaded(BanFlip, player, amount, duration)
