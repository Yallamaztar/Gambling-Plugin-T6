from core.database.bank import BankManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit

class DailyClaimCommand:
    def __init__(self, player: str) -> None:
        amount = 150_000
        BankManager().deposit(player, amount)
        Wrapper().commands.privatemessage(player, f"^2Successfully ^7claimed ^5${amount}")
        return

class WeeklyClaimCommand:
    def __init__(self, player: str) -> None:
        amount = 5_000_000
        BankManager().deposit(player, amount)
        Wrapper().commands.privatemessage(player, f"^2Successfully ^7claimed ^5${amount}")
        return

class MonthlyClaimCommand:
    def __init__(self, player: str) -> None:
        amount = 100_000_000
        BankManager().deposit(player, amount)
        Wrapper().commands.privatemessage(player, f"^2Successfully ^7claimed ^5${amount}")
        return

@rate_limit(hours=24)
def daily(player: str) -> None:
    run_command_threaded(DailyClaimCommand, player)

@rate_limit(hours=168) # Week
def weekly(player: str) -> None:
    run_command_threaded(WeeklyClaimCommand, player)

@rate_limit(hours=720) # Month
def monthly(player: str) -> None:
    run_command_threaded(MonthlyClaimCommand, player)