from core.database.bank import BankManager
from core.database.admins import AdminManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit

from typing import Optional

class ShopCommand:
    def __init__(self, player: str, item: Optional[str] = None, target: Optional[str] = None) -> None:
        self.commands = Wrapper().commands
        self.bank     = BankManager()
        self.player   = player
        
        allowed_maps = [ 
            "carrier", "express", "hijacked", "overflow", "plaza", 
            "raid", "slums", "standoff", "turbine", "yemen", "mr" 
        ]

        if item is None or item == "":
            self.show_shop(); return

        if target:
            if target.lower() in allowed_maps: self.map = target
            else:
                self.target = Wrapper().player.find_player_by_partial_name(target)
                if not self.target:
                    self.commands.privatemessage(player, f"{target} not found"); return

        self.buy_item(item.lower())
    
    def show_shop(self) -> None:
        shop = {
            1: "^7[1] ^5Fast^7Restart Map  - $200t",
            2: "^7[2] ^5Gambler ^7Role     - $10q",
            3: "^7[3] ^5Map ^7Change       - $550q",
            4: "^7[4] ^5SeniorAdmin ^7Role - $100,000z",
            5: "^7[5] ^5Gambling ^7Admin   - $50,000z",
        }
        
        self.commands.privatemessage(self.player, "^7-- ^5Brow^7nies ^5Shop ^7--")
        for _, item in shop.items(): 
            self.commands.privatemessage(self.player, item)

    def buy_item(self, item: str) -> None:
        if item in [ "fastrestart", "fr", "1" ]:
            price = 200_000_000_000_000
            balance = self.bank.balance(self.player)

            if balance == 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return
            
            if balance < price: 
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1{price - balance}^7)"); return
            
            self.bank.deposit(self.player, -price)
            self.commands.fastrestart()

        elif item in [ "gambler", "gambla", "2" ]:
            price = 10_000_000_000_000 # 10q
            balance = self.bank.balance(self.player)
            
            if balance == 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return

            if balance < price: 
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1{price - balance}^7)"); return
            
            self.bank.deposit(self.player, -price)

            if self.target: 
                self.commands.setlevel(self.target, "trusted")
                self.commands.privatemessage(self.player, f"Promoted {self.target} to ^2Certified Gambla"); return
            
            self.commands.setlevel(self.player, "trusted")
            self.commands.privatemessage(self.player, "You have been ^3promoted ^7to ^2Gambler")
        
        elif item in [ "mapchange", "map", "3" ]:
            price = 550_000_000_000_000_000 # 500q
            balance = self.bank.balance(self.player)

            if balance == 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return

            if balance < price: 
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1{price - balance}^7)"); return

            self.bank.deposit(self.player, -price)
            self.commands.change_map(self.map)

        elif item in [ "senioradmin", "sr", "4" ]:
            price = 100_000_000_000_000_000_000_000 # 100,000z
            balance = self.bank.balance(self.player)
            
            if balance == 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return

            if balance < price:
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1{price - balance}^7)"); return
            
            self.bank.deposit(self.player, -price)

            if self.target:
                self.commands.setlevel(self.target, "administrator")
                self.commands.privatemessage(self.player, f"Promoted {self.target} to ^6SeniorAdmin"); return

            self.commands.setlevel(self.player, "administrator")
            self.commands.privatemessage(self.player, "You have been ^3promoted ^7to ^2SeniorAdmin")
        
        elif item in [ "administrator", "admin", "5" ]:
            price = 50_000_000_000_000_000_000_000 # 50,000z
            balance = self.bank.balance(self.player)

            if balance == 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return
            
            if balance < price: 
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1{price - balance}^7)"); return
            
            self.bank.deposit(self.player, -price)

            if self.target:
                AdminManager().add(self.target)
                self.commands.privatemessage(self.player, f"Promoted {self.target} to ^5Gambling Admin")
                self.commands.privatemessage(self.target, f"You have been ^3promoted ^7to ^2Gambling Admin By {self.player}"); return
            
            AdminManager().add(self.player)
            self.commands.privatemessage(self.player, "You have been ^3promoted ^7to ^2Gambling Admin")

        elif item in [ "randomeffect", "effect", "6" ]:
            price = 5_000_000_000
            balance = self.bank.balance(self.player)

            if balance == 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return
            
            if balance < price: 
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1{price - balance}^7)"); return
            
            self.bank.deposit(self.player, -price)

            effects = [
                "TakeWeapons",
                "GiveWeapon"
                "TeamSwitch",
                "Kill",
                "SetSpectator",
                "PlayerToMe",
                "LockControls",
                "m"
            ]

        else: 
            self.commands.privatemessage(self.player, "Invalid item selected"); return

@rate_limit(seconds=5)
def shop(player: str, item: Optional[str] = None, target: Optional[str] = None) -> None:
    run_command_threaded(ShopCommand, player, item, target)