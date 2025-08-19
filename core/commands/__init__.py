from functools import wraps
from typing import Optional, Dict, Callable, Any
from threading import Thread, Lock
import time

from core.database.owners import OwnerManager
from core.wrapper import Wrapper
from core.utils import format_time

def rate_limit(*, 
    hours: Optional[int] = None, 
    minutes: Optional[int] = None, 
    seconds: Optional[int] = None
) -> Callable:
    
    if hours is None and minutes is None and seconds is None:
        raise ValueError("missing hours, minutes or seconds")
    
    rate_limit_time: int = (hours or 0) * 3600 + (minutes or 0) * 60 + (seconds or 0)
    threads: Dict[tuple, Lock] = {}
    last_call: Dict[tuple, float] = {}

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(player: str, *args, **kwargs) -> Any:
            if player in OwnerManager().load():
                return func(player, *args, **kwargs)

            now = now = time.time()
            key = (func.__name__, player)

            if key not in threads:
                threads[key] = Lock()
                last_call[key] = 0.0

            with threads[key]:
                if now - last_call[key] < rate_limit_time:
                    remaining = int(rate_limit_time - (now - last_call[key]))
                    Wrapper().commands.privatemessage(player, f"^7You must wait ^3{format_time(remaining)} ^7before using this again")
                    return
                last_call[key] = now

            return func(player, *args, **kwargs)
        return wrapper
    return decorator

def run_command_threaded(cls, *args, **kwargs):
    Thread(target=lambda: cls(*args, **kwargs), daemon=True).start()