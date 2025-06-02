from functools import wraps
from typing import List, Callable, Any
from threading import Thread

from core.database.owners import OwnerManager
from core.wrapper import Wrapper

def owners_only(owners: List[str] = OwnerManager().load()) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, player: str, *args, **kwargs) -> Any:
            if player not in owners:
                Wrapper().commands.privatemessage(player, "You ^1don't^7 have the ^3permission ^7to use this command")
                return
            return func(self, player, *args, **kwargs)
        return wrapper
    return decorator

def run_command_threaded(cls, *args, **kwargs):
    Thread(target=lambda: cls(*args, **kwargs), daemon=True).start()