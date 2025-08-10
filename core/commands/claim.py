from core.database.bank import BankManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit

class HourlyClaimCommand:
    def __init__(self, player: str) -> None:
        amount = 5000
        BankManager().deposit(player, amount)
        Wrapper().commands.privatemessage(player, f"^2Successfully ^7claimed ^5${amount}")

class DailyClaimCommand:
    def __init__(self, player: str) -> None:
        amount = 50000
        BankManager().deposit(player, amount)
        Wrapper().commands.privatemessage(player, f"^2Successfully ^7claimed ^5${amount}")

class WeeklyClaimCommand:
    def __init__(self, player: str) -> None:
        amount = 450_000
        BankManager().deposit(player, amount)
        Wrapper().commands.privatemessage(player, f"^2Successfully ^7claimed ^5${amount}")

class MonthlyClaimCommand:
    def __init__(self, player: str) -> None:
        amount = 4_000_000
        BankManager().deposit(player, amount)
        Wrapper().commands.privatemessage(player, f"^2Successfully ^7claimed ^5${amount}")

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