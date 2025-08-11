from core.database.bank import BankManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit

class ClaimCommand:
    def __init__(self, player: str, amount: int) -> None:
        self.bank     = BankManager()
        self.commands = Wrapper().commands

        self.player = player
        self.amount = amount

        self.claim()

    def claim(self) -> None:
        self.bank.deposit(self.player, self.amount)
        self.commands.privatemessage(self.player, f"^2Successfully ^7claimed ^5${self.amount}")

class HourlyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        super().__init__(player, 5_000)

class DailyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        super().__init__(player, 50_000)

class WeeklyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        super().__init__(player, 450_000)

class MonthlyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        super().__init__(player, 4_000_000)


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