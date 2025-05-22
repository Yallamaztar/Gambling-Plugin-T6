from typing import List, Tuple, Optional, Callable
from core.db import Bank
from core.utils import parse_amount
from iw4m import IW4MWrapper
import random

class Register:
    def __init__(self, owner: str, *, bank: Bank, server: IW4MWrapper.Server, player: IW4MWrapper.Player, commands: IW4MWrapper.Commands, prefix: Optional[str] = "!") -> None:
        self.owner    = owner
        self.bank     = bank
        self.server   = server
        self.player   = player
        self.commands = commands
        self.prefix   = prefix

        self._handlers: List[Tuple[str, Callable]] = []
        self.impl_commands()

    def register_command(self, command: str, *, callback: Callable) -> None:
        self._handlers.append((command, callback))

    def impl_commands(self) -> None:
        def balance(player: str) -> None:
            bal = self.bank.get_balance(player)
            self.commands.privatemessage(player, f"your balance is ^1${bal}")

        def gamble(player: str, amount: str) -> None:
            try:
                bet = parse_amount(amount)
                current = self.bank.get_balance(player)

                if current < bet:
                    self.commands.privatemessage(player, f"^1cannot^7 bet ${bet}, you ^3only^7 have ^1${current}")

                if random.choice([True, False]):
                    self.bank.deposit(player, bet * 2)
                    result = "^2won^7"
                else:
                    self.bank.deposit(player, -bet)
                    result = "^1lost^7"

                new_balance = self.bank.get_balance(player)
                self.commands.privatemessage(player, f"you {result}, new balance: ^1${new_balance}")

            except ValueError:
                self.commands.privatemessage(player, f"{bet} ^1is not^7 a valid number")

        def pay(player: str, target: str, amount: str) -> None:
            try:
                amount = parse_amount(amount)
                if amount <= 0:
                    self.commands.privatemessage(player, f"^1cannot pay^7 non-positive amount: {amount}")

                current = self.bank.get_balance(player)
                if current < amount:
                    self.commands.privatemessage(player, f"^1cannot pay^7 ${amount}, you ^3only^7 have ^1${current}")

                self.bank.deposit(player, -amount)
                self.bank.deposit(target, amount)

                player_new_balance = self.bank.get_balance(player)
                target_new_balance = self.bank.get_balance(target)

                self.commands.privatemessage(player, f"you paid ^2${amount}^7 to {target}, new balance: ^1${player_new_balance}")
                self.commands.privatemessage(target, f"{player} paid you ^2${amount}^7, new balance: ^1${target_new_balance}")

            except ValueError:
                self.commands.privatemessage(player, f"^1{amount}^7 is ^1not^7 a valid number")

        def give(player: str, target: str, amount: str) -> None:
            if player != self.owner:
                self.commands.privatemessage(player, "you dont have ^1perms^7 for this")
                return

            target = self.player.find_player_by_partial_name(target)

            self.bank.deposit(target, parse_amount(amount))
            self.commands.privatemessage(player, f"gave {target} ${amount}")
            self.commands.privatemessage(player, f"you got ${amount}")

        self.register_command(f"{self.prefix}gamble",  callback=gamble)
        self.register_command(f"{self.prefix}balance", callback=balance)
        self.register_command(f"{self.prefix}pay",     callback=pay)
        self.register_command(f"{self.prefix}give",    callback=give)
