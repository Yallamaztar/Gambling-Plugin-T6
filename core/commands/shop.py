from core.database.bank import BankManager
from core.database.links import LinkManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit

from typing import Optional
import random

class ShopCommand:
    def __init__(self, player: str, item: Optional[str] = None, target: Optional[str] = None) -> None:
        print(f"[ShopCommand] {player} {item} {target if target != None else ''}")
        if not LinkManager().is_linked(player):
            Wrapper().commands.privatemessage(player, "^1You must link your Discord account to use this command. Use ^3!link ^1to link your account.")
            return
        
        self.commands = Wrapper().commands
        self.bank     = BankManager() 
        self.player   = player
        
        allowed_maps = [ 
            "carrier", "express", "hijacked", "overflow", "plaza", 
            "raid", "slums", "standoff", "turbine", "yemen", "mr" 
        ]

        if item is None or item == "":
            self.show_shop(); return

        self.target = None; self.map = None

        if target:
            if target.lower() in allowed_maps: self.map = target
            else:
                self.target = Wrapper().player.find_player_by_partial_name(target)
                if not self.target:
                    self.commands.privatemessage(player, f"{target} not found"); return

        self.buy_item(item.lower())
    
    def show_shop(self) -> None:
        shop = {
            1: "^7[1] ^5Fast^7Restart Map  - $500t",
            2: "^7[2] ^5Gambler ^7Role     - $40q",
            3: "^7[3] ^5Map ^7Change       - $10q",
            4: "^7[4] ^5SeniorAdmin ^7Role - $150,000y",
            5: "^7[5] ^5Random ^7Effect    - $50t",
            6: "^7[6] ^5Kill ^7Player      - $10z"
        }
        
        self.commands.privatemessage(self.player, "^7-- ^5Brow^7nies ^5Shop ^7--")
        for _, item in shop.items(): 
            self.commands.privatemessage(self.player, item)

    def buy_item(self, item: str) -> None:
        if item in [ "fastrestart", "fr", "1" ]:
            price = 500_000_000_000_000
            balance = self.bank.balance(self.player)

            if balance <= 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return
            
            if balance < price: 
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1${price - balance}^7)"); return
            
            self.bank.deposit(self.player, -price)
            self.commands.fastrestart()

        elif item in [ "gambler", "gambla", "2" ]:
            price = 40_000_000_000_000 # 40q
            balance = self.bank.balance(self.player)
            
            if balance <= 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return

            if balance < price: 
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1${price - balance}^7)"); return
            
            self.bank.deposit(self.player, -price)

            if self.target: 
                self.commands.setlevel(self.target, "trusted")
                self.commands.privatemessage(self.player, f"Promoted {self.target} to ^2Certified Gambla"); return
            
            self.commands.setlevel(self.player, "trusted")
            self.commands.privatemessage(self.player, "You have been ^3promoted ^7to ^2Gambler")
        
        elif item in [ "mapchange", "map", "3" ]:
            price = 10_000_000_000_000_000 # 10q
            balance = self.bank.balance(self.player)

            if balance <= 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return

            if balance < price: 
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1${price - balance}^7)"); return

            self.bank.deposit(self.player, -price)
            self.commands.change_map(self.map) # type: ignore

        elif item in [ "senioradmin", "sr", "4" ]:
            price = 150_000_000_000_000_000_000_000_000_000 # 150,000y
            balance = self.bank.balance(self.player)
            
            if balance <= 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return

            if balance < price:
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1${price - balance}^7)"); return
            
            self.bank.deposit(self.player, -price)

            if self.target:
                self.commands.setlevel(self.target, "administrator")
                self.commands.privatemessage(self.player, f"Promoted {self.target} to ^6SeniorAdmin"); return

            self.commands.setlevel(self.player, "administrator")
            self.commands.privatemessage(self.player, "You have been ^3promoted ^7to ^2SeniorAdmin")
        
        elif item in [ "randomeffect", "random", "effect", "5" ]:
            price = 50_000_000_000_000 # 50t
            balance = self.bank.balance(self.player)

            if balance <= 0:
                self.commands.say(f"^7@{self.player} us ^1^Fgay n poor"); return

            if balance < price:
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1${price - balance}^7)"); return

            self.bank.deposit(self.player, -price)
            helper = ShopHelper(self.player, price)

            effects = [
                lambda: self.commands.takeweapons(self.player),
                lambda: self.commands.kill(self.player),
                lambda: self.commands.giveweapon(self.player, "ballist_mp+dualclip+is"),
                lambda: self.commands.say(f"^7@{self.player} rolled a random effect and won nothing! Congratulations"),
                lambda: helper.double_money(),
                lambda: helper.loose_double_money()
            ]

            random.choice(effects)() 
        
        # elif item in [ "administrator", "admin", "5" ]:
        #     price = 550_000_000_000_000_000_000_000_000 # 550,000o
        #     balance = self.bank.balance(self.player)

        #     if balance <= 0:
        #         self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return
            
        #     if balance < price: 
        #         self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1${price - balance}^7)"); return
            
        #     self.bank.deposit(self.player, -price)

        #     if self.target:
        #         AdminManager().add(self.target)
        #         self.commands.privatemessage(self.player, f"Promoted {self.target} to ^5Gambling Admin")
        #         self.commands.privatemessage(self.target, f"You have been ^3promoted ^7to ^2Gambling Admin By {self.player}"); return
            
        #     AdminManager().add(self.player)
        #     self.commands.privatemessage(self.player, "You have been ^3promoted ^7to ^2Gambling Admin")

        elif item in [ "killplayer", "kpl", "6" ]:
            price = 10_000_000_000_000_000_000 # 10z
            balance = self.bank.balance(self.player)

            if balance <= 0:
                self.commands.say(f"^7@{self.player} is ^1^Fgay n poor"); return
            
            if balance < price: 
                self.commands.privatemessage(self.player, f"You cant ^1afford ^7this (missing ^1${price - balance}^7)"); return           

            self.bank.deposit(self.player, -price)
            self.commands.kill(self.target)

            self.commands.privatemessage(self.target, f"You got killed by {self.player}")

        else: 
            self.commands.privatemessage(self.player, "Invalid item selected"); return

class ShopHelper:
    def __init__(self, player: str, price: int):
        self.bank     = BankManager()
        self.commands = Wrapper().commands

        self.player = player
        self.price  = price
        
    def double_money(self) -> None:
        self.bank.deposit(self.player, int(self.price * 2))
        self.commands.privatemessage(self.player, f"You just won ^5${int(self.price * 2)}")

    def loose_double_money(self) -> None:
        self.bank.deposit(self.player, -int(self.price * 2))
        self.commands.privatemessage(self.player, f"You just lost ^1${int(self.price * 2)}")

@rate_limit(seconds=5)
def shop(player: str, item: Optional[str] = None, target: Optional[str] = None) -> None:
    run_command_threaded(ShopCommand, player, item, target)
