from core.database.bank import BankManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit
from core.utils import parse_prefix_amount

import time

class RichestCommand:
    def __init__(self, player: str) -> None:
        print(f"[RichestCommand] {player}")
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.commands.say("^7Top 5 ^5richest ^7players:")
        time.sleep(.5)
        for i, p in enumerate(self.bank.top_balances()):
            self.commands.say(f"^7#{i + 1} {p['name']} - ^5${parse_prefix_amount(int(p['balance']))}^7") 
            time.sleep(.2)

@rate_limit(seconds=15)
def richest(player: str) -> None:
    run_command_threaded(RichestCommand, player)