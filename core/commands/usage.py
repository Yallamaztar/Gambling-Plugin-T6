from core.commands import run_command_threaded
from core.wrapper import Wrapper
import time
from typing import Optional

class UsageCommand:
    def __init__(self, player: str, page: Optional[str] = None ) -> None:
        if not page or page == "1":
            Wrapper().commands.privatemessage(player, "-- ^3Usage ^7Page ^51/3 --")
            Wrapper().commands.privatemessage(
                player, "^7!gamble <amount> - ^250/50^7 chance to double or lose your bet"
            ); time.sleep(.5)

            Wrapper().commands.privatemessage(
                player, "^7!balance or !bal <player (optional)> - ^2Check your or another's balance"
            );time.sleep(.5)

            Wrapper().commands.privatemessage(
                player, "^7!pay <player> <amount> - ^2Send money to another player"
            ); time.sleep(.5)

            Wrapper().commands.privatemessage(
                player, "^7!richest - ^2See the top 5 richest players"
            ); time.sleep(.5)

            Wrapper().commands.privatemessage(
                player, "^7Type ^3!usage 2 ^7for claiming commands!"
            ); time.sleep(.5)
        
        elif page == "2":
            Wrapper().commands.privatemessage(player, "-- ^3Usage ^7Page ^52/3 --")
            Wrapper().commands.privatemessage(
                player, "^7Use ^3k^7, ^3m^7, ^3b^7, ^3t^7, ^3q^7 or ^3z^7 (e.g., 5k, 2m) for amounts"
            ); time.sleep(.5)

            Wrapper().commands.privatemessage(player, "^5Daily Claims:")
            Wrapper().commands.privatemessage(
                player, "^7!daily - Claim ^2$1,000,000 ^7(24h cooldown)"
            ); time.sleep(.5)

            Wrapper().commands.privatemessage(
                player, "^7!weekly - Claim ^2$15,000,000 ^7(7 days cooldown)"
            ); time.sleep(.5)

            Wrapper().commands.privatemessage(
                player, "^7!monthly - Claim ^2$100,000,000 ^7(30 days cooldown)"
            ); time.sleep(.5)

            Wrapper().commands.privatemessage(
                player, "^7Type ^3!usage 3 ^7for admin commands!"
            ); time.sleep(.5)
        
        elif page == "3":
            Wrapper().commands.privatemessage(player, "-- ^3Usage ^7Page ^53/3 --")
            Wrapper().commands.privatemessage(player, "^1Admin Commands:"); time.sleep(.5)

            Wrapper().commands.privatemessage(
                player, "^7!give <player> <amount> - ^1Give money to a player"
            ); time.sleep(.5)
            
            Wrapper().commands.privatemessage(
                player, "^7!giveall <amount> - ^1Give money to all players"
            ); time.sleep(.5)
            
            Wrapper().commands.privatemessage(
                player, "^7!take <player> <amount> - ^1Take money from a player"
            ); time.sleep(.5)
            
            Wrapper().commands.privatemessage(
                player, "^7!takeall <amount> - ^1Take money from all players"
            ); time.sleep(.5)
            
            Wrapper().commands.privatemessage(
                player, "^7!reset - ^1Reset all bank accounts"
            ); time.sleep(.5)
            
            Wrapper().commands.privatemessage(
                player, "^7!addowner/!removeowner <player> - ^1Manage owners"
            ); time.sleep(.5)
        
        return
    
def usage(player: str, page: Optional[str] = None) -> None:
    run_command_threaded(UsageCommand, player, page)