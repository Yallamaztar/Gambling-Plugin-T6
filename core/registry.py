from typing import List, Tuple, Optional, Callable
from iw4m import IW4MWrapper
import random

from core.db import Bank

class Register:
    def __init__(self, owner: str, *, server: IW4MWrapper.Server, player: IW4MWrapper.Player, commands: IW4MWrapper.Commands, prefix: Optional[str] = "!") -> None:
        self.owner    = owner
        self.bank     = Bank()
        self.server   = server
        self.player   = player
        self.commands = commands
        self.prefix   = prefix

        self._handlers: List[Tuple[str, Callable]] = []
        self.impl_commands()

    def register_command(self, command: str, *, callback: Callable) -> None:
        self._handlers.append((command, callback))

    def parse_amount(self, amount: str) -> int:
        if amount[-1].lower() == 'k':
            return int(float(amount[:-1]) * 1000)
        elif amount[-1].lower() == 'm':
                return int(float(amount[:-1]) * 1000000)
        elif amount[-1].lower() == 'b':
            return int(float(amount[:-1]) * 1000000000)
        elif amount[-1].lower() == 't':
            return int(float(amount[:-1]) * 1000000000000)
        else:
            return int(amount)

    def impl_commands(self) -> None:
        def balance(player: str, target: Optional[str] = None) -> None:
            if target == None:
                bal = self.bank.get_balance(player)
                self.commands.privatemessage(player, f"your balance is ^1${bal}")
            else:
                bal = self.bank.get_balance(self.player.find_player_by_partial_name(target))
                self.commands.privatemessage(player, f"{target}'s balance is ^1${bal}")

        def gamble(player: str, amount: str) -> None:
            try:
                if amount == "all":    
                    bet = self.bank.get_balance(player)
                    if bet == 0: 
                        self.commands.say(f"^7@{player} is ^1^Fgay n poor")
                        return
                    
                else:
                    bet = self.parse_amount(amount)
                    current = self.bank.get_balance(player)

                    if current < bet:
                        self.commands.privatemessage(player, f"^1cannot^7 bet ${bet}, you ^3only^7 have ^1${current}")
                        return
                
                    if bet <= 0:
                        self.commands.privatemessage(player, f"^1cannot pay^7 non-positive amount: {amount}")
                        return
                
                win = random.choice([True, False])
                if win:
                    self.bank.deposit(player, bet)
                    result = "^2won^7"
                else:
                    self.bank.deposit(player, -bet)
                    result = "^1lost^7"

                new_balance = self.bank.get_balance(player)
                self.commands.privatemessage(player, f"you {result}, new balance: ^1${new_balance}")
                self.commands.say(f"^7{player} {result} ${bet}")

            except ValueError:
                self.commands.privatemessage(player, f"{amount} ^1is not^7 a valid number")
            
        def pay(player: str, target: str, amount: str) -> None:
            try:
                amount = self.parse_amount(amount)
                if amount <= 0:
                    self.commands.privatemessage(player, f"^1cannot pay^7 non-positive amount: {amount}")
                    return
                
                current = self.bank.get_balance(player)
                if current < amount:
                    self.commands.privatemessage(player, f"^1cannot pay^7 ${amount}, you ^3only^7 have ^1${current}")
                    return
                
                self.bank.deposit(player, -amount)

                target = self.player.find_player_by_partial_name(target)
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

            self.bank.deposit(target, self.parse_amount(amount))
            self.commands.privatemessage(player, f"gave {target} ${amount}")
            self.commands.privatemessage(target, f"you got ${amount}")
        
        def take(player: str, target: str, amount: str) -> None:
            if player != self.owner:
                self.commands.privatemessage(player, "you dont have ^1perms^7 for this")
                return
            
            target = self.player.find_player_by_partial_name(target)

            if amount == "all":
                amount = self.bank.get_balance(target)
            else:
                amount = self.parse_amount(amount)
                current = self.bank.get_balance(target)

                if amount > current:
                    self.commands.privatemessage(player, f"^1cannot^7 take {amount} from {target}")
                    return
            
            self.bank.deposit(target, -amount)
            self.commands.privatemessage(player, f"took ${amount} from player")
            self.commands.privatemessage(target, f"{player} took ${amount} from you")

        def give_all(player: str, amount: str) -> None:
            if player != self.owner:
                self.commands.privatemessage(player, "you dont have ^1perms^7 for this")
                return
            
            for p in self.server.get_players():
                self.bank.deposit(p['name'], self.parse_amount(amount))
                self.commands.privatemessage(player, f"gave {p['name']} ${amount}")
                self.commands.privatemessage(p['name'], f"you got ${amount}")

        def take_all(player: str):
            if player != self.owner:
                self.commands.privatemessage(player, "you dont have ^1perms^7 for this")
                return
            
            players = self.server.get_players()
            self.commands.say(f"^7Taking {len(players)} players moneys")

            for p in players:
                current = self.bank.get_balance(p['name'])
                if current == 0:
                    return
                
                self.bank.deposit(p['name'], -current)
                self.commands.privatemessage(player, f"Took {len(players)} players money")

        self.register_command(f"{self.prefix}gamble",  callback=gamble)
        self.register_command(f"{self.prefix}balance", callback=balance)
        self.register_command(f"{self.prefix}pay",     callback=pay)
        self.register_command(f"{self.prefix}give",    callback=give)
        self.register_command(f"{self.prefix}take",    callback=take)
        self.register_command(f"{self.prefix}giveall", callback=give_all)
        self.register_command(f"{self.prefix}takeall", callback=take_all)