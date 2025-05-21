from typing import List, Tuple, Optional, Callable
from core.db import Bank
import random

class Register:
    def __init__(self, bank: Bank, *, prefix: Optional[str] = "!") -> None:
        self.bank   = bank
        self.prefix = prefix

        self._handlers: List[Tuple[str, Callable]] = []
        self.impl_commands()

    def register_command(self, command: str, *, callback: Callable) -> None:
        self._handlers.append((command, callback))

    def impl_commands(self) -> None:
        def balance(player: str) -> Tuple[str, int]: 
            return player, f"your balance is ^1${self.bank.get_balance(player)}"

        def gamble(player: str, amount: str) -> Tuple[str, str]: 
            try: 
                bet = int(amount)
                current = self.bank.get_balance(player)
                if current < bet:
                    return player, f"^1cannot bet^7 ${bet}, you ^3only^7 have ^1${current}"
                
                if random.choice([True, False]):
                    self.bank.deposit(player, bet * 2)
                    result = "^2won^7"
                else:
                    self.bank.deposit(player, -bet)
                    result = "^1lost^7"

                new_balance = self.bank.get_balance(player)
                return player, f"you {result}, new balance: ^1${new_balance}"
            
            except ValueError:
                return player, f"{bet} ^1is not^7 a valid number"

        self.register_command(f"{self.prefix}gamble",  callback=gamble)
        self.register_command(f"{self.prefix}balance", callback=balance)