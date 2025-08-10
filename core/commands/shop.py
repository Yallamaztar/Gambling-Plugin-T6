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
            self.commands.privatemessage(player, "More Stuff Coming In Future!")
        
        elif item.lower() == "trusted":
            price = int(500_000_000)
            balance = self.bank.balance(player)
            
            if balance < price: 
                self.commands.privatemessage(player, "You cant ^1afford ^7this")
                return
            
            else:
                self.bank.deposit(player, -price)
                self.commands.setlevel(player, "trusted")
                self.commands.privatemessage(player, "Congratulations! You have been ^3promoted ^7to ^2Gambler")

        elif item.lower() == "senioradmin":
            price = int(100_000_000_000_000_000) # 100 zillion or wtv
            balance = self.bank.balance(player)
            
            if balance < price:
                self.commands.privatemessage(player, "You cant ^1afford ^7this")
                return
            
            else:
                self.bank.deposit(player, -price)
                self.commands.setlevel(player, "senioradmin")
                self.commands.privatemessage(player, "Congratulations! You have been ^3promoted ^7to ^2SeniorAdmin")
        
        return


def shop(player: str, item: Optional[str] = None) -> None:
    run_command_threaded(ShopCommand, player, item)