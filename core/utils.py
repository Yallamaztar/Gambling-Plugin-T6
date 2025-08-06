import re, random
from typing import Optional

def safe_int(value: str, default: Optional[int] = 0) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def parse_amount(amount: str) -> int:
    prefixes = {"k": 1000, "m": 1000000, "b": 1000000000, "t": 1000000000000, "q": 1000000000000000, "z":1000000000000000000}

    amount = amount.lower().strip()
    if amount[-1] in prefixes:
        return safe_int(amount[:-1]) * prefixes[amount[-1]]
    else:
        return safe_int(amount)

def split_clan_tag(name: str) -> str:
    match = re.match(r"^(\[[^\[\]]{1,10}\])(.+)", name)
    if match:
        return f"^{random.randint(0, 9)}{match.group(1)}^7{match.group(2)}"
    return name.strip()

def format_time(seconds: int) -> str:
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m {seconds % 60}s"
    
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"