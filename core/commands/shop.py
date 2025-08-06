from core.database.bank import BankManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded

from typing import Optional

class ShopCommand:
    def __init__(self, player: str, item: Optional[str] = None) -> None:
        self.commands = Wrapper().commands
        self.bank = BankManager()

        if item is None or item == "":
            self.commands.privatemessage(player, "^7-- ^5Brow^7nies ^5Shop ^7--")
            self.commands.privatemessage(player, "^^5Gambler ^7Role - $10bil")
            self.commands.privatemessage(player, "^8SeniorAdmin ^7Role - $100z")
            self.commands.privatemessage(player, "")
        
        elif item.lower() == "trusted":
            balance = self.bank.balance(player)
            
            if balance < 500_000_000: 
                self.commands.privatemessage(player, "You cant ^1afford ^7this")
                return
            else:
                self.bank.deposit(player, -10_000_000_000)
                self.commands.setlevel(player, "trusted")
                self.commands.privatemessage(player, "Congratulations! You have been ^3promoted ^7to ^2Trusted")

        elif item.lower() == "senioradmin":
            balance = self.bank.balance(player)
            
            if balance < 100_000_000_000_000_000:
                self.commands.privatemessage(player, "You cant ^1afford ^7this")
                return
            else:
                self.bank.deposit(player, -100_000_000_000_000_000_000)
                self.commands.setlevel(player, "senioradmin")
                self.commands.privatemessage(player, "Congratulations! You have been ^3promoted ^7to ^2SeniorAdmin")

def shop(player: str, item: Optional[str] = None) -> None:
    run_command_threaded(ShopCommand, player, item)