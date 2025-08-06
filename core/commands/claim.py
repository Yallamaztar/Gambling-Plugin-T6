from core.database.bank import BankManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit

class DailyClaimCommand:
    def __init__(self, player: str) -> None:
        amount = 1000000
        BankManager().deposit(player, amount)
        Wrapper().commands.say(f"^2Successfully ^7claimed ^5${amount}")
        return

class WeeklyClaimCommand:
    def __init__(self, player: str) -> None:
        amount = 15000000
        BankManager().deposit(player, amount)
        Wrapper().commands.say(f"^2Successfully ^7claimed ^5${amount}")
        return

class MonthlyClaimCommand:
    def __init__(self, player: str) -> None:
        amount = 100000000
        BankManager().deposit(player, amount)
        Wrapper().commands.say(f"^2Successfully ^7claimed ^5${amount}")
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