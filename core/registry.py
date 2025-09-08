from core.commands.owner import add_owner, remove_owner
from core.commands.balance import balance
from core.commands.gamble import gamble
from core.commands.give import give, give_all, admin_give, admin_give_all
from core.commands.pay import pay
from core.commands.reset import reset
from core.commands.rich import richest
from core.commands.take import take, take_all
from core.commands.usage import usage
from core.commands.claim import hourly, daily, weekly, monthly
from core.commands.shop import shop 
from core.commands.banflip import banflip
from core.commands.link import link
from core.commands.admin import add_admin, remove_admin

from typing import List, Tuple, Optional, Callable

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

        # Shop command
        self.register_command(f"{self.prefix}shop", alias=f"{self.prefix}shp", callback=shop)

        # Discord link
        self.register_command(f"{self.prefix}link", alias=f"{self.prefix}lnk", callback=link)

        # Admin commands
        self.register_command(f"{self.prefix}give",        alias=f"{self.prefix}gi",  callback=admin_give)
        self.register_command(f"{self.prefix}giveall",     alias=f"{self.prefix}ga",  callback=admin_give_all)

        # Owner commands
        self.register_command(f"{self.prefix}give",        alias=f"{self.prefix}gi",  callback=give)
        self.register_command(f"{self.prefix}giveall",     alias=f"{self.prefix}ga",  callback=give_all)
        self.register_command(f"{self.prefix}take",        alias=f"{self.prefix}t",   callback=take)
        self.register_command(f"{self.prefix}takeall",     alias=f"{self.prefix}ta",  callback=take_all)
        self.register_command(f"{self.prefix}reset",       alias=f"{self.prefix}res", callback=reset)

        self.register_command(f"{self.prefix}addadmin",    alias=f"{self.prefix}aa", callback=add_admin)
        self.register_command(f"{self.prefix}removeadmin", alias=f"{self.prefix}ra", callback=remove_admin)
        self.register_command(f"{self.prefix}addowner",    alias=f"{self.prefix}add", callback=add_owner)
        self.register_command(f"{self.prefix}removeowner", alias=f"{self.prefix}rmv", callback=remove_owner)
