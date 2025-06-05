from core.database.bank import BankManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded

import time

class StatsCommand:
    def __init__(self, player: str) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.bank = BankManager()

        self.commands.say("^7Top 5 ^5richest ^7players:")
        time.sleep(.5)
        for i, player in enumerate(self.bank.top_balances()):
            self.commands.say(f"^7#{i + 1} {player['name']} - ^5{player['balance']}")
            time.sleep(.2)

        return

def stats(player: str) -> None:
    run_command_threaded(StatsCommand, player)