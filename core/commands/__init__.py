from functools import wraps
from typing import Dict, List, Callable, Any
from threading import Thread, Lock
import time

from core.database.owners import OwnerManager
from core.wrapper import Wrapper
from core.utils import format_time

def rate_limit(*, hours: int = None, minutes: int = None) -> Callable:
    if hours == None and minutes == None:
        raise ValueError("missing hours or minutes")
    
    rate_limit_time: int = (hours or 0) * 3600 + (minutes or 0) * 60
    threads: Dict[str, Lock] = {}
    last_call: Dict[str, float] = {}

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, player, *args, **kwargs) -> Any:
            if player in OwnerManager().load():
                return
            
            now = time.monotonic()
            
            if player not in threads:
                threads[player] = Lock()
                last_call[player] = 0.0

            with threads[player]:
                if now - last_call[player] < rate_limit_time:
                    remaining = int(rate_limit_time) - int((now - last_call[player]))
                    Wrapper().commands.privatemessage(self, f"You must wait {format_time(remaining)}s before using this again")
                    return
                
                last_call[player] = now
            return func(self, player, *args, **kwargs)
        return wrapper
    return decorator

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