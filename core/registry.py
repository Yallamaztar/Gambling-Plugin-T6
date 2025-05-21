from typing import List, Tuple, Optional, Callable
from core.db import Bank
from core.utils import printdebug, printinfo, printerror, parse_amount
from iw4m import IW4MWrapper
import random

class Register:
    def __init__(self, bank: Bank, commands: IW4MWrapper.Commands, *, prefix: Optional[str] = "!") -> None:
        self.bank     = bank
        self.commands = commands
        self.prefix   = prefix

        self._handlers: List[Tuple[str, Callable]] = []
        self.impl_commands()
        
    def register_command(self, command: str, *, callback: Callable) -> None:
        self._handlers.append((command, callback))

    def impl_commands(self) -> None:
        def balance(player: str) -> Tuple[str, int]: 
            printdebug(f"balance function executed for: {player}")
            bal = self.bank.get_balance(player)
            printinfo(f"{player} checked their balance: ${bal}")
            return player, f"your balance is ^1${bal}"

        def gamble(player: str, amount: str) -> Tuple[str, str]: 
            printdebug(f"{player} started gamble with amount: {amount}")
            try: 
                bet = parse_amount(amount)
                current = self.bank.get_balance(player)
                printinfo(f"{player}'s current balance: ${current}")

                if current < bet:
                    printerror(f"{player} tried to bet ${bet} but only has ${current}")
                    return player, f"^1cannot bet^7 ${bet}, you ^3only^7 have ^1${current}"
                
                win = random.choice([True, False])
                printdebug(f"gamble outcome for {player}: {'win' if win else 'loss'}")
                
                if win:
                    self.bank.deposit(player, bet * 2)
                    result = "^2won^7"
                    printinfo(f"{player} won the bet, gained ${bet * 2}")
                else:
                    self.bank.deposit(player, -bet)
                    result = "^1lost^7"
                    printinfo(f"{player} lost the bet, lost ${bet}")

                new_balance = self.bank.get_balance(player)
                printdebug(f"{player}'s new balance: ${new_balance}")
                return player, f"you {result}, new balance: ^1${new_balance}"
            
            except ValueError:
                printerror(f"{player} entered invalid bet amount: {amount}")
                return player, f"{bet} ^1is not^7 a valid number"

        def pay(player: str, target: str, amount: str) -> Tuple[str, str]:
            printdebug(f"{player} attempts to pay {target} amount: {amount}")
            try:
                amount = parse_amount(amount)
                if amount <= 0:
                    printerror(f"{player} tried to pay non-positive amount: {amount}")
                    return player, f"^1cannot pay^7 non-positive amount: {amount}"

                current = self.bank.get_balance(player)
                printinfo(f"{player}'s current balance: ${current}")

                if current < amount:
                    printerror(f"{player} tried to pay ${amount} but only has ${current}")
                    return player, f"^1cannot pay^7 ${amount}, you ^3only^7 have ^1${current}"

                self.bank.deposit(player, -amount)
                self.bank.deposit(target, amount)

                printinfo(f"{player} paid ${amount} to {target}")
                player_new_balance = self.bank.get_balance(player)
                target_new_balance = self.bank.get_balance(target)
                printdebug(f"{player}'s new balance: ${player_new_balance}")
                printdebug(f"{target}'s new balance: ${target_new_balance}")
                self.commands.privatemessage(target, f"{player} paid you ^2${amount}^7, new balance: ^1${target_new_balance}")
                return player, f"you paid ^2${amount}^7 to {target}. New balance: ^1${player_new_balance}"

            except ValueError:
                printerror(f"{player} entered invalid pay amount: {amount}")
                return player, f"{amount} ^1is not^7 a valid number"

        self.register_command(f"{self.prefix}gamble",  callback=gamble)
        self.register_command(f"{self.prefix}balance", callback=balance)
        self.register_command(f"{self.prefix}pay",     callback=pay)