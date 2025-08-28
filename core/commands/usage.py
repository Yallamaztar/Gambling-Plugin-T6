from core.commands import run_command_threaded
from core.wrapper import Wrapper
from core.permissions import discord_linked_only

import time
from typing import Optional

USAGE_PAGES = {
    "1": [
        "^7-- ^3Usage ^7Page ^51^7/^46 --",
        "^3!gamble ^7or !g ^7<amount> - ^245^7/^155^7 chance to win (with 5% house fee)",
        "^3!highrisk ^7or !hr ^7<amount> - ^335^7/^165^7 chance to win 2.5x (with 15% house fee)",
        "^3!balance ^7or !bal ^7<player (optional)> - ^5Check ^7your or another players balance",
        "^3!pay ^7<player> <amount> - ^5Send ^7money to another player",
        "^3!richest ^7- See the ^5top 5 ^7richest players",
        "^3Use ^3k^7, ^3m^7, ^3b^7, ^3t^7, ^3q^7 or ^3z^7 (e.g, 5k, 2m) for amounts",
    ],
    "2": [
        "^7-- ^3Usage ^7Page ^52^7/^46 --",
        "^5Daily Claims^7:",
        "^3!hourly ^7- Claim ^2$5,000 ^7(1h cooldown)",
        "^3!daily ^7- Claim ^2$50_000 ^7(24h cooldown)",
        "^3!weekly ^7- Claim ^2$450_000 ^7(7 days cooldown)",
        "^3!monthly ^7- Claim ^2$4_000_000 ^7(30 days cooldown)",
    ],
    "3": [
        "^7-- ^3Usage ^7Page ^53^7/^46 --",
        "^3!bf ^7250k ^55d ^7- Bet $250,000, risk a 5-day ban if you lose",
        "^3!bf ^7all ^530m ^7- Bet everything you own, 30-minute ban on loss",
        "^3!bf ^7half ^52h ^7- Bet half your balance, 2-hour ban on loss",
        "The longer the ^1ban ^7the ^5bigger ^7the ^5multiplier!",
        "^1Note: ^7Banflip has 40% win rate with 10% house fee",
    ],
    "4": [
        "^7-- ^3Usage ^7Page ^54^7/^46 --",
        "^5Shop Commands^7:",
        "^3!shop ^7- Open the shop menu",
        "^3!shop ^7<item_number> - ^5Purchase ^7an item or role",
        "^7Example: ^3!shop 1 ^7to buy the Gambler role",
    ],
    "5": [
        "^7-- ^3Usage ^7Page ^55^7/^46 --",
        "^5Betting Limits^7:",
        "^3!gamble all ^7- Maximum 80% of your balance",
        "^3!highrisk all ^7- Maximum 60% of your balance",
        "^3!banflip all ^7- Maximum 70% of your balance",
        "^7House always has an edge - gamble responsibly!",
    ],
    "6": [
        "^7-- ^3Usage ^7Page ^56^7/^46 --",
        "^5Other tips^7:",
        "^7Use ^3!help ^7<command> for detailed info on any command",
        "^7Check your balance regularly with ^3!balance ^7to avoid ^1surprises",
        "^7Use shorthand amounts like ^35k^7 for 5,000 or ^32m^7 for 2,000,000",
        "^7Join the community Discord for help! (discord.gg/DtktFBNf5T)",
    ]
}

class UsageCommand:
    def __init__(self, player: str, page: Optional[str] = None ) -> None:
        commands = Wrapper().commands
        key = page if page in USAGE_PAGES else "1"

        for line in USAGE_PAGES[key]:
            commands.privatemessage(player, line)
            time.sleep(.25)

@discord_linked_only()
def usage(player: str, page: Optional[str] = None) -> None:
    run_command_threaded(UsageCommand, player, page)