from typing import List, Tuple, Optional, Callable
from iw4m import IW4MWrapper

from core.database.bank import BankManager
from core.commands.balance import balance
from core.commands.gamble import gamble
from core.commands.give import give, give_all
from core.commands.pay import pay
from core.commands.reset import reset
from core.commands.stats import stats
from core.commands.take import take, take_all
from core.commands.usage import usage

class Register:
    def __init__(self, prefix: Optional[str] = "!") -> None:
        self.prefix = prefix
        self._handlers: List[Tuple[str, Callable]] = []
        self.impl_commands()

    def register_command(self, command: str, *, alias: str, callback: Callable) -> None:
        self._handlers.append((command, alias, callback))

    def impl_commands(self) -> None:
        self.register_command(f"{self.prefix}usage",   alias=f"{self.prefix}u",    callback=usage)
        self.register_command(f"{self.prefix}gamble",  alias=f"{self.prefix}g",    callback=gamble)
        self.register_command(f"{self.prefix}balance", alias=f"{self.prefix}bal",  callback=balance)
        self.register_command(f"{self.prefix}pay",     alias=f"{self.prefix}p",    callback=pay)
        self.register_command(f"{self.prefix}give",    alias=f"{self.prefix}g",    callback=give)
        self.register_command(f"{self.prefix}richest", alias=f"{self.prefix}rich", callback=stats)
        self.register_command(f"{self.prefix}take",    alias=f"{self.prefix}t",    callback=take)
        self.register_command(f"{self.prefix}giveall", alias=f"{self.prefix}ga",   callback=give_all)
        self.register_command(f"{self.prefix}takeall", alias=f"{self.prefix}ta",   callback=take_all)
        self.register_command(f"{self.prefix}reset",   alias=f"{self.prefix}res",  callback=reset)
