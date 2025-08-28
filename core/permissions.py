from core.database.owners import OwnerManager
from core.database.admins import AdminManager
from core.database.links import LinkManager
from core.wrapper import Wrapper

from typing import Callable, Any
from functools import wraps

class PermissionManager:
    def __init__(self) -> None:
        self.owners = OwnerManager().get_all()
        self.admins = AdminManager().get_all()

    def is_owner(self, player: str) -> bool:
        return player in self.owners
    
    def is_admin(self, player: str) -> bool:
        return player in self.admins or self.is_owner(player)
    
    def reload(self) -> None:
        self.owners = OwnerManager().get_all()
        self.admins = AdminManager().get_all()

def discord_linked_only() -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, player: str, *args, **kwargs) -> Any:
            print(f"[DiscordLinkedOnly] {self}")
            if not LinkManager().is_linked(player) and not PermissionManager().is_owner(player):
                Wrapper().commands.privatemessage(player, "^1You must link your Discord account to use this command. Use ^3!link ^1to link your account.")
                return
            return func(self, player, *args, **kwargs)
        return wrapper
    return decorator

def owners_only() -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, player: str, *args, **kwargs) -> Any:
            print(f"[OwnersOnly] {player}")
            if not PermissionManager().is_owner(player):
                Wrapper().commands.privatemessage(player, "You ^1don't^7 have the ^3permission ^7to use this command")
                return
            return func(self, player, *args, **kwargs)
        return wrapper
    return decorator

def admins_only() -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, player: str, *args, **kwargs) -> Any:
            print(f"[AdminsOnly] {player}")
            if not PermissionManager().is_admin(player):
                Wrapper().commands.privatemessage(player, "You ^1don't^7 have the ^3permission ^7to use this command")
                return
            return func(self, player, *args, **kwargs)
        return wrapper
    return decorator