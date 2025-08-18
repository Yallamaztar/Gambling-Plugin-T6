from core.database.bank import BankManager
from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit

class ClaimCommand:
    def __init__(self, player: str, amount: int) -> None:
        Wrapper().player.player_rank_from_name(player)
        BankManager().deposit(player, amount)
        Wrapper().commands.privatemessage(player, f"^2Successfully ^7claimed ^5${amount}")

class HourlyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        super().__init__(player, 100_000)

class DailyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        super().__init__(player, 1_500_000)

class WeeklyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        super().__init__(player, 12_500_000)

class MonthlyClaimCommand(ClaimCommand):
    def __init__(self, player: str) -> None:
        super().__init__(player, 100_000_000)

# Trusted role only aka certified gambla (brownies reference fr)
class RoleClaimDaily(ClaimCommand):
    def __init__(self, player: str, role: str) -> None:
        if role != "Trusted": return
        super().__init__(player, 5_000_000)

class RoleClaimWeekly(ClaimCommand):
    def __init__(self, player: str, role: str) -> None:
        if role != "Trusted": return
        super().__init__(player, 17_000_000)


@rate_limit(hours=24)
def role_daily(player: str) -> None:
    run_command_threaded(RoleClaimDaily, player)


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