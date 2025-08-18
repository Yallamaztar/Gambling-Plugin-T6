from typing import List, Tuple, Optional, Callable

from core.commands.owner import add_owner, remove_owner
from core.commands.balance import balance
from core.commands.gamble import gamble
from core.commands.give import give, give_all
from core.commands.pay import pay
from core.commands.reset import reset
from core.commands.rich import richest
from core.commands.take import take, take_all
from core.commands.usage import usage
from core.commands.claim import hourly, daily, weekly, monthly, role_daily, role_weekly
from core.commands.shop import shop 
from core.commands.banflip import banflip
from core.commands.link import link

class Register:
    def __init__(self, prefix: Optional[str] = "!") -> None:
        self.prefix = prefix
        self._handlers: List[Tuple[str, str, Callable]] = []
        self.register_commands()
        print(f"[Register] {len(self._handlers)} Commands registered")
    
    def register_command(self, command: str, *, alias: str, callback: Callable) -> None:
        self._handlers.append((command.lower(), alias.lower(), callback))

    def register_commands(self) -> None:
        # Client commands
        self.register_command(f"{self.prefix}usage",   alias=f"{self.prefix}u",    callback=usage)
        self.register_command(f"{self.prefix}gamble",  alias=f"{self.prefix}g",    callback=gamble)
        self.register_command(f"{self.prefix}balance", alias=f"{self.prefix}bal",  callback=balance)
        self.register_command(f"{self.prefix}pay",     alias=f"{self.prefix}p",    callback=pay)
        self.register_command(f"{self.prefix}richest", alias=f"{self.prefix}rich", callback=richest)
        self.register_command(f"{self.prefix}banflip", alias=f"{self.prefix}bf",   callback=banflip)

        # Claimable commands
        self.register_command(f"{self.prefix}hourly",  alias=f"{self.prefix}hrl",  callback=hourly)
        self.register_command(f"{self.prefix}daily",   alias=f"{self.prefix}day",  callback=daily)
        self.register_command(f"{self.prefix}weekly",  alias=f"{self.prefix}wkly", callback=weekly)
        self.register_command(f"{self.prefix}monthly", alias=f"{self.prefix}mnth", callback=monthly)

        # Claimable (role) commands
        self.register_command(f"{self.prefix}dailyCertified",  alias="dc", callback=role_daily)
        self.register_command(f"{self.prefix}weeklyCertified", alias="wc", callback=role_weekly)

        # Shop command
        self.register_command(f"{self.prefix}shop", alias=f"{self.prefix}shp", callback=shop)

        # Discord link
        self.register_command(f"{self.prefix}link", alias=f"{self.prefix}lnk", callback=link)

        # Admin commands
        self.register_command(f"{self.prefix}give",        alias=f"{self.prefix}gi",  callback=give)
        self.register_command(f"{self.prefix}giveall",     alias=f"{self.prefix}ga",  callback=give_all)
        self.register_command(f"{self.prefix}take",        alias=f"{self.prefix}t",   callback=take)
        self.register_command(f"{self.prefix}takeall",     alias=f"{self.prefix}ta",  callback=take_all)
        self.register_command(f"{self.prefix}reset",       alias=f"{self.prefix}res", callback=reset)
        self.register_command(f"{self.prefix}addowner",    alias=f"{self.prefix}add", callback=add_owner)
        self.register_command(f"{self.prefix}removeowner", alias=f"{self.prefix}rmv", callback=remove_owner)