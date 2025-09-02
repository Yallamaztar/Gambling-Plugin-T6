from core.database.bank import BankManager
from core.database.links import LinkManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit
from core.utils import parse_prefix_amount

class ClaimCommand:
    def __init__(self, player: str, amount: int) -> None:
        print(f"[ClaimCommand] {player} ${amount}")
        if not LinkManager().is_linked(player):
            Wrapper().commands.privatemessage(player, "^1You must link your Discord account to use this command. Use ^3!link ^1to link your account.")
            return
        
        BankManager().deposit(player, amount)
        Wrapper().commands.privatemessage(player, f"^2Successfully ^7claimed ^5${parse_prefix_amount(amount)}")

class HourlyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        if not LinkManager().is_linked(player):
            Wrapper().commands.privatemessage(player, "^1You must link your Discord account to use this command. Use ^3!link ^1to link your account.")
            return
        
        super().__init__(player, 100_000)

class DailyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        if not LinkManager().is_linked(player):
            Wrapper().commands.privatemessage(player, "^1You must link your Discord account to use this command. Use ^3!link ^1to link your account.")
            return
        
        super().__init__(player, 1_500_000)

class WeeklyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        if not LinkManager().is_linked(player):
            Wrapper().commands.privatemessage(player, "^1You must link your Discord account to use this command. Use ^3!link ^1to link your account.")
            return
        
        super().__init__(player, 12_500_000)

class MonthlyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        if not LinkManager().is_linked(player):
            Wrapper().commands.privatemessage(player, "^1You must link your Discord account to use this command. Use ^3!link ^1to link your account.")
            return
        
        super().__init__(player, 100_000_000)

@rate_limit(hours=1)
def hourly(player: str) -> None:
    run_command_threaded(HourlyClaimCommand, player)

@rate_limit(hours=24)
def daily(player: str) -> None:
    run_command_threaded(DailyClaimCommand, player)

@rate_limit(hours=168) # Week
def weekly(player: str) -> None:
    run_command_threaded(WeeklyClaimCommand, player)

@rate_limit(hours=720) # Month
def monthly(player: str) -> None:
    run_command_threaded(MonthlyClaimCommand, player)