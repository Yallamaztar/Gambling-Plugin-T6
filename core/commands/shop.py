from core.database.bank import BankManager
from core.database.owners import OwnerManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit
from typing import Optional

class ShopCommand:
    def __init__(self, player: str, item: Optional[str] = None) -> None:
        self.commands = Wrapper().commands
        self.bank     = BankManager()

        if item is None or item == "": self.show_shop(player)
        else: self.buy_item(player, item)
    
    def show_shop(self, player: str) -> None:
        self.commands.privatemessage(player, "^7-- ^5Brow^7nies ^5Shop ^7--")
        self.commands.privatemessage(player, "^7[1] ^5Fast^7Restart Map  - $150m")
        self.commands.privatemessage(player, "^7[3] ^5Gambler ^7Role     - $10b")
        self.commands.privatemessage(player, "^7[4] ^5SeniorAdmin ^7Role - $250q")
        self.commands.privatemessage(player, "^7[5] ^5Gambling ^7Owner   - $100z")

    def buy_item(self, player: str, item: str) -> None:
        if item.lower() == "fastrestart" or item.lower() == "fr" or item == "1":
            price = 150_000_000
            balance = self.bank.balance(player)

            if balance == 0:
                self.commands.say(f"^7@{player} is ^1^Fgay n poor"); return
            
            if balance < price: 
                self.commands.privatemessage(player, "You cant ^1afford ^7this"); return
            
            self.bank.deposit(player, -price)
            self.commands.fastrestart()

        elif item.lower() == "gambler" or item == "2":
            price = 500_000_000_000 # 500 billion
            balance = self.bank.balance(player)
            
            if balance == 0:
                self.commands.say(f"^7@{player} is ^1^Fgay n poor"); return

            if balance < price: 
                self.commands.privatemessage(player, "You cant ^1afford ^7this"); return
            
            self.bank.deposit(player, -price)
            self.commands.setlevel(player, "trusted")
            self.commands.privatemessage(player, "Congratulations! You have been ^3promoted ^7to ^2Gambler")
        
        elif item.lower() == "senioradmin" or item.lower() == "sr" or item == "3":
            price = 100_000_000_000_000_000_000 # 100 zillion or wtv
            balance = self.bank.balance(player)
            
            if balance == 0:
                self.commands.say(f"^7@{player} is ^1^Fgay n poor"); return

            if balance < price:
                self.commands.privatemessage(player, "You cant ^1afford ^7this"); return
            
            self.bank.deposit(player, -price)
            self.commands.setlevel(player, "senioradmin")
            self.commands.privatemessage(player, "Congratulations! You have been ^3promoted ^7to ^2SeniorAdmin")
        
        elif item.lower() == "owner" or item == "4":
            price = 400_000_000_000_000_000_000
            balance = self.bank.balance(player)

            if balance == 0:
                self.commands.say(f"^7@{player} is ^1^Fgay n poor"); return
            
            if balance < price: 
                self.commands.privatemessage(player, "You cant ^1afford ^7this"); return
            
            self.bank.deposit(player, -price)
            OwnerManager().add(player)
            self.commands.privatemessage(player, "Congratulations! You have been ^3promoted ^7to ^2Gambling Admin")

        else: 
            self.commands.privatemessage(player, "Invalid item selected"); return

@rate_limit(seconds=5)
def shop(player: str, item: Optional[str] = None) -> None:
    run_command_threaded(ShopCommand, player, item)