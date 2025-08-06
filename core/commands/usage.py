from core.commands import run_command_threaded
from core.wrapper import Wrapper
import time

class UsageCommand:
    def __init__(self, player: str) -> None:
        Wrapper().commands.privatemessage(player, "^7!gamble <amount> - ^250/50^7 chance to double or lose your bet")
        time.sleep(.5)
        Wrapper().commands.privatemessage(player, "^7!balance or !bal <player (optional)> - ^2Check your or another's balance")
        time.sleep(.5)
        Wrapper().commands.privatemessage(player, "^7!pay <player> <amount> - ^2Send money to another player")
        time.sleep(.5)
        Wrapper().commands.privatemessage(player, "^7!richest - ^2See the top 5 richest players")
        time.sleep(.5)
        Wrapper().commands.privatemessage(player, "^7Use ^3k^7, ^3m^7, ^3b^7, ^3t^7, ^3q^7 or ^3z^7 (e.g., 5k, 2m) for amounts")
        return
    
def usage(player: str) -> None:
    run_command_threaded(UsageCommand, player)